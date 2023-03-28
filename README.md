# Taux de rénovation des archétypes de bâtiments Danube

La base de données Danube a été construite dans le cadre du projet Mapuce, finalisé en 2015. **Danube décrit le parc immobilier de manière archétypale**, c'est-à-dire les principales tendances de dispositifs constructifs sont associées à des groupes des bâtiments aux caractéristiques similaires (les archétypes), en considérant les pratiques constructives et architecturales couramment employées en France métropolitaine. 

Cette base de données est utilisée pour des simulations de microclimat, notamment pour les calculs des températures en ville, puisque le parc immobilier contribue aux phénomènes d’îlot de chaleur. Danube décrivait les caractéristiques des bâtiments au moment de leur construction, sans tenir compte des rénovations successives qui ont pu avoir lieu. **La rénovation du parc immobilier modifie la dynamique des échanges thermiques entre les bâtiments et son l'environnement**, ce qui peut avoir un impact significatif sur les simulations microclimatiques. 

Ce travail consiste à **enrichir Danube en prenant en compte les rénovations** qui ont pu avoir lieu aux bâtiments répresentés par les archétypes Danube. Pour ce faire, les Diagnostiques de Performance Energétique (DPE) disponibles dans la Base de Données Nationale des Bâtiments (BDNB) ont été utilisés. Dans un premier temps, un **mappage et filtrage des archétypes Danube** a été réalisé sur des données geolocalisées (_/preprocessing_data_). Ces **données geolocalisées** ont été le résultat d'une jointure spatiale de 4 jeux de données (ci-dessous) et ne peuvent être partagées pour des raisons de droits: 
- La carte de territoires Mapuce
- La BDNB v0.64 (version ayant droit aux fichier fonciers)
- Des cartes typologigues geoclimate (si possible)
- Filosofi v2015 produite par l'INSEE

Dans la suite, les **valeurs U des dispositifs Danube** ont été calculées avec la **méthode DPE 3CL 2012** en considérant la matérialité des archétypes Danube pour déterminer les seuils de la rénovation (_/data_analysis/danube_u_value_ranges_). Finalement, des **analyses statistiques** ont été appliqués pour étudier le **niveau de rénovation** des échantillons d'archétypes Danube (_/data_analysis/statistics_assembled_archetypes_). Cette analyse  s'est déroulée selon les étapes suivantes : 
- Des **statistiques descriptives** pour des valeur U des archétypes Danube acompagnées par ses plots de distrubutions avec les seuils utilisés pour déterminér la rénovation (_/analysis_density_distribution_). 
- L'étude de la **matérialité des archétypes** de chaque échantillon des données géolocalisés (_/resume_wall_roof_windows_)
- **Teste de Kolmogorov–Smirnov** pour déterminer si les échantillons avec une même U-valeur des dispositifs Danube appartenaient à la même distribution de probabilité (_/kolmogorov_smirnov_test_). 
- **Teste Chi² pour étudier la relation entre la rénovation des bâtiments et des indicateur sociologigiques** sur les revenus des ménages (taux de pauvreté et taux de proprietaires) de la base de données Filosofi (_/sociological_indicators_filosofi_).
