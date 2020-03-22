# CAD_effectifs


## Problème général: 

créer des équipages ayant différents types de compétences, sur un planning d'une semaine.

## Infos colonnes:
- anon : identifiant des personnes disponibles

- dispo : dates de dispo : ne prendre en compte que la colonne reformatée "dispo",représentant le début d'une plage horaire de 2h, à laquelle est associée une valeur OUI ou NON, selon la disponibilité ou non de la personne sur cette plage horaire

- VALUE : valeur associée à la plage horaire, indique si la personne est disponible ou non

- les autres colonnes sont les compétences, avec un booléen pour savoir si le benevole l'a


## Equipages :
- Renfort Samu : plage horaire de 6 à 12h - compétences :  1 ci, 1 chauf_vpsp, 1 ou 2 PSE2

- VLUMS : plage horaire de 6 à 12h - 2 PSE(1 ou 2) - idealement un chauffeur_vl

- croix rouge chez vous : plage horaire de 4 à 12h - 2 benevoles (pas de compétences particulières) - idealement un chauffeur_vl 

## Choix : 
- maximiser le nombre de renforts samu, puis le nombre de VLUMS, puis le nombre de croix rouge chez vous

- les compétences critiques sont les ci et les chauffeurs vpsp (moins nombreux)

- garder au maximum les ci et les chauffeurs vpsp pour ne faire que ca. S'ils sont CI et chauffeur vpsp, à voir en fonction des besoins de la plage horaire.


## Plus d'infos contraintes, et plus facile du coup:
cf fichier csv que j'ajoute : equipages.csv



Un grand merci pour votre aide!
