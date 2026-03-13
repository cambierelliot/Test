Penser Data Access / Data Product -> Pr faciliter l'accès à la donnée -> pr préparer nos plateformes data à consommer les données 
First step : socle GCP en application avec le projet hubble (lien Abir) 
et après voir comment on ouvre le sujet sur l'on premise 
Bien avoir en tête l'open source aussi 
 
à regarder : 
Semantic : étude des contrats : https://bitol-io.github.io/open-data-contract-standard/v3.1.0/ à comparer https://www.snowflake.com/en/blog/osi-initiative-expands-partners/
Semantic dans GCP https://medium.astrafy.io/bigquerys-native-semantic-layer-the-graph-approach-4ba8aa3aa965?gi=5cf8c4327c2d -> PM vision ? 
Graphe : Graphe Context usages dans les agent 
Agent : Decision runtime 
Reprise des travaux de Julien : Dataplex et ADK 
AGENT Starburst -> à regarder mais l'idée est plutôt de créer l'agent 
NB : Starburst en mode proxy 
MCP BQ -> synchro Greg 
Definition: Open Data Contract Standard (ODCS) - Open Data Contract Standard
Details of the Open Data Contract Standard (ODCS). Includes fundamentals, datasets, schemas, data quality, pricing, stakeholders, roles, service-level agreements and other properties.


1. Le Constat & Le Besoin (Le "Pourquoi")
Historique : Notre écosystème est fragmenté. La donnée brute est dans les bases (On-Prem/Cloud), les métadonnées techniques dans Atlas, et le glossaire métier dans Zeenea.

Le problème : Avec l'avènement des LLMs et de l'interrogation sémantique, cette fragmentation freine l'accès à la donnée et limite la compréhension du contexte par les IA.

L'objectif global : Unifier et sémantiser cet écosystème pour rendre la donnée facilement consommable par des LLMs et des utilisateurs finaux.

2. Le Terrain de Jeu : Le Projet "Hubble" (Le "Quoi")
Utiliser le projet Hubble (données open source) comme bac à sable.

L'enjeu : Construire un "Proof of Concept" (PoC) d'une nouvelle architecture unifiée.

Le but final : Faire une démonstration percutante pour "vendre" cette nouvelle architecture aux autres entités du groupe.

3. Les Chantiers Techniques Cloud / GCP (Le "Comment")
Standardisation via l'Open Source : * Faire une étude et une présentation détaillée de l'ODCS (Open Data Contract Standard).

Objectif : Implémenter ces contrats de données sur le projet Hubble.

Architecture GCP & Sémantique : * Déployer la "Semantic Layer" dans GCP.

Focus Dataplex : Comprendre en profondeur Dataplex pour l'articuler au centre de cette nouvelle architecture (gouvernance, qualité, catalogue unifié).

4. La Démonstration de Valeur : Approche PM & Agents IA
Adopter une vision Produit (PM) : Ne pas faire de la tech pour de la tech, mais prouver l'utilité métier.

Le test comparatif (A/B Testing d'architecture) : * Créer un Agent 1 (Basique, branché sur l'architecture actuelle/ancienne).

Créer un Agent 2 (Avancé, branché sur la nouvelle architecture Hubble + Dataplex + Couche sémantique).

But : Démontrer visuellement et techniquement la supériorité de la nouvelle archi (meilleures réponses, plus de contexte métier).

5. Perspectives & Améliorations Futures (Le "Next Step")
Amélioration de l'Agent Cloud : * Intégrer du "Graph Context" pour que l'agent comprenne les relations complexes entre les données.

Ajouter du "Decision Runtime" (ex: inspiration Rippletide) pour contrôler et guider les actions de l'agent.

Ouverture vers le On-Premise :

Une fois le modèle GCP prouvé, collaborer avec le collègue travaillant sur l'intégration MCP (Model Context Protocol) et Starburst.

Objectif : Étendre cette nouvelle vision unifiée aux données hébergées sur nos propres serveurs (On-Prem).



Penser Data Access / Data Product -> Pr faciliter l'accès à la donnée -> pr préparer nos plateformes data à consommer les données 
First step : socle GCP en application avec le projet hubble (lien Abir) 
et après voir comment on ouvre le sujet sur l'on premise 
Bien avoir en tête l'open source aussi 
 
à regarder : 
Semantic : étude des contrats : https://bitol-io.github.io/open-data-contract-standard/v3.1.0/ à comparer https://www.snowflake.com/en/blog/osi-initiative-expands-partners/
Semantic dans GCP https://medium.astrafy.io/bigquerys-native-semantic-layer-the-graph-approach-4ba8aa3aa965?gi=5cf8c4327c2d -> PM vision ? 
Graphe : Graphe Context usages dans les agent 
Agent : Decision runtime 
Reprise des travaux de Julien : Dataplex et ADK 
AGENT Starburst -> à regarder mais l'idée est plutôt de créer l'agent 
NB : Starburst en mode proxy 
MCP BQ -> synchro Greg 
Definition: Open Data Contract Standard (ODCS) - Open Data Contract Standard
Details of the Open Data Contract Standard (ODCS). Includes fundamentals, datasets, schemas, data quality, pricing, stakeholders, roles, service-level agreements and other properties.
on a des demandes sur le chat to data -> es tu ready pr démo et explication archi actuelle ? meme si on a des next steps (api conv etc...) on a déjà une vision d'archi qui se confirme meme chez microsoft avec l'apparition de Fabric IQ pour la semantic ahha
 
on a  BPA, paiement qui sont chauds en bilat à avoir une démo + je pense qu'on fera un petit brief en commu GCP 
 
