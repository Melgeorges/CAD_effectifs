
import pandas as pd
from datetime import datetime

# data non anonymisée
infos = pd.read_csv("/home/melanie/Documents/croixrouge/data/20200323-ResOP consolidée.csv", delimiter=":")

# modif que j'ai réalisées
competence = infos["Quelle sont vos compétences Croix-Rouge ?"]
competence = competence.fillna("aucune")

chauffeur_vl = [True if "Chauffeur VL" in elem else False for elem in competence]
PSE1 = [True if "PSE1" in elem else False for elem in competence]
PSE2 = [True if "PSE2" in elem else False for elem in competence]
chauf_vpsp = [True if "Chauffeur VPSP" in elem else False for elem in competence]
maraud = [True if "Maraudeur.se" in elem else False for elem in competence]
psc1 = [True if "PSC1" in elem else False for elem in competence]
log = [True if "Logisticien.ne Croix-Rouge" in elem else False for elem in competence]
chef_maraud = [True if "Chef.fe d'équipe maraudes" in elem else False for elem in competence]
fle = [True if "Animateur.rice de cours de FLE" in elem else False for elem in competence]
perm_soc = [True if "Responsable Permanence Sociale" in elem else False for elem in competence]
ci = [True if "CI" in elem else False for elem in competence]
nouv_bene = [True if "Nouveau bénévole" in elem else False for elem in competence]
infirmier = [True if "Infirmier.e local.e" in elem else False for elem in competence]
tsa = [True if "TSA / Coreg" in elem else False for elem in competence]



infos = infos.assign(chauffeur_vl=chauffeur_vl,
                     PSE1=PSE1,
                     PSE2=PSE2,
                     chauf_vpsp=chauf_vpsp,
                     maraud=maraud,
                     psc1=psc1,
                     log=log,
                     chef_maraud=chef_maraud,
                     fle=fle,
                     perm_soc=perm_soc,
                     ci=ci,
                     nouv_bene=nouv_bene,
                     tsa=tsa,
                     infirmier=infirmier)

cols = ['Horodateur', 'Adresse e-mail', 'Numéro de téléphone portable', 'Prénom', 'NOM', 'Votre structure de rattachement', 'Unnamed: 6',
        'Cadre ?', 'Secouriste ?', 'Si oui, quelle est-elle ?', 'Quelle sont vos compétences Croix-Rouge ?',
        'Quelle est votre profession ?', "Uniforme ?",
        'chauffeur_vl', 'PSE1', 'PSE2', 'chauf_vpsp', 'maraud', 'psc1', 'log', 'chef_maraud', 'fle', 'perm_soc', 'ci', 'nouv_bene',
        'tsa', 'infirmier', 'Unnamed: 97']

mapping_days = {'Lundi': "2020-03-23",
                'Mardi': "2020-03-24",
                'Mercredi': "2020-03-25",
                'Jeudi': "2020-03-26",
                'Vendredi': "2020-03-27",
                'Samedi': "2020-03-28",
                'Dimanche': "2020-03-29"}

anon_dict = dict([(y,x) for x,y in enumerate(set(infos.NOM))])

infos_rowed = infos.melt(id_vars=cols,
                         var_name="Date",
                         value_name="Value")

infos_rowed.Date = [elem.replace(" ", "") for elem in infos_rowed.Date]
infos_rowed.Date = [elem.replace("[", "") for elem in infos_rowed.Date]
infos_rowed.Date = [elem.replace("]", "") for elem in infos_rowed.Date]
infos_rowed["day_name"] = [elem.split("-")[0] for elem in infos_rowed.Date]
infos_rowed["day"] = infos_rowed["day_name"].replace(mapping_days)
infos_rowed["hour_dispo"] = [elem.split("-")[1]+':00' for elem in infos_rowed.Date]
infos_rowed['dispo'] = infos_rowed[['day', 'hour_dispo']].agg(' '.join, axis=1)


infos_rowed['anon'] = infos_rowed.NOM.replace(anon_dict)
to_send = infos_rowed[['anon', 'chauffeur_vl', 'PSE1', 'PSE2', 'chauf_vpsp', 'maraud', 'psc1', 'log',
                       'chef_maraud', 'fle', 'perm_soc', 'ci', 'nouv_bene', 'tsa', 'infirmier',
                       'Date', 'Value', 'day_name', 'dispo']]
to_send.to_csv("anonymise_competence_dispos.csv")




# que pour mel
infos_rowed['anon'] = infos_rowed.NOM
to_send = infos_rowed[['anon', 'chauffeur_vl', 'PSE1', 'PSE2', 'chauf_vpsp', 'maraud', 'psc1', 'log',
                       'chef_maraud', 'fle', 'perm_soc', 'ci', 'nouv_bene', 'tsa', 'infirmier',
                       'Date', 'Value', 'day_name', 'dispo']]

to_send.to_csv("competence_dispos.csv")