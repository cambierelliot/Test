# import google.generativeai as genai
import requests

# 1. Configuration de ton agent Google (Gemini)
# Tu lui déclares l'outil (la fonction) qu'il a le droit d'utiliser
model = genai.GenerativeModel(
    model_name='gemini-2.5-pro',
    tools=[declaration_outil_remboursement] # Ta déclaration d'outil
)

# 2. L'utilisateur fait une demande
response = model.generate_content("Rembourse 50€ pour la commande CMD-123.")

# 3. INTERCEPTION : Gemini veut utiliser un outil !
if response.function_call:
    nom_outil = response.function_call.name
    arguments = type(response.function_call.args).to_dict(response.function_call.args)
    
    print(f"🤖 Gemini propose d'exécuter : {nom_outil} avec {arguments}")
    
    # 4. LA DOUANE : On demande à Rippletide avant d'aller plus loin
    decision_rippletide = requests.post(
        "https://agent.rippletide.com/api/sdk/action/evaluate",
        headers={"x-api-key": "TA_CLE_RIPPLETIDE"},
        json={"action_name": nom_outil, "parameters": arguments}
    ).json()
    
    # 5. L'EXÉCUTION DÉTERMINISTE
    if decision_rippletide.get("approved") == True:
        # FEU VERT : Ton code exécute la vraie action
        resultat_reel = executer_vrai_remboursement_stripe(arguments)
        
        # Tu renvoies le succès à Gemini pour qu'il finisse sa phrase
        reponse_finale = model.generate_content(f"Succès de l'outil : {resultat_reel}")
        
    else:
        # FEU ROUGE : Rippletide a bloqué l'action
        raison = decision_rippletide.get("reason")
        print(f"❌ Rippletide a bloqué l'action : {raison}")
        
        # Tu renvoies l'échec à Gemini pour qu'il explique le refus à l'utilisateur
        reponse_finale = model.generate_content(
            f"L'outil a été bloqué par les règles métier. Raison: {raison}. Explique-le à l'utilisateur."
        )

print(reponse_finale.text)
