# Renovation rate of Danube building archetypes

The Danube database was built as part of the Mapuce project, completed in 2015. **Danube describes the building stock in an archetypal manner**, i.e. the main trends in construction methods are associated with groups of buildings with similar characteristics (archetypes), taking into account the construction and architectural practices commonly used in mainland France. 

This database is used for microclimate simulations, particularly for calculating urban temperatures, since the building stock contributes to heat island phenomena. Danube described the characteristics of buildings at the time they were constructed, without taking into account any successive renovations that may have taken place. **Renovation of the building stock modifies the dynamics of heat exchanges between buildings and their environment**, which can have a significant impact on microclimatic simulations. 

This work consists of **enriching Danube by taking into account the renovations** that may have taken place to the buildings represented by the Danube archetypes. To do this, the Energy Performance Diagnostics (DPE) available in the National Buildings Database (BDNB) were used. Firstly, a **mapping and filtering of the Danube archetypes** was carried out on geolocalised data (_/preprocessing_data_). This **geospatial data** was the result of a spatial join of 4 datasets (below) and cannot be shared for rights reasons: 
- Mapuce territory map
- The BDNB v0.64 (version submitted to rights)
- Geoclimate layer of building typology (if possible)
- Filosofi v2015 produced by INSEE

Subsequently, the **U-values of the Danube devices** were calculated using the **DPE 3CL 2012 method**, taking into account the materiality of the Danube archetypes to determine the renovation thresholds (_/data_analysis/danube_u_value_ranges_). Finally, **statistical analyses** were applied to study the **level of renovation** of the samples of Danube archetypes (_/data_analysis/statistics_assembled_archetypes_). This analysis was carried out in the following stages: 
- **Descriptive statistics** for the U-values of the Danube archetypes accompanied by their plots of distributions with the thresholds used to determine renovation (_/analysis_density_distribution_). 
- The study of the **materiality of the archetypes** of each sample of geospatial data (_/resume_wall_roof_windows_)
- **Kolmogorov-Smirnov test** to determine whether different U-value samples share a significantly similar probability distribution (_/kolmogorov_smirnov_test_). 
- **Chi² test to study the relationship between building renovation and sociological indicators**, poverty rate and homeownership rate, from the Filosofi database (_/sociological_indicators_filosofi_).

__________________________________________________________________________________


# Taux de rénovation des archétypes de bâtiments Danube

La base de données Danube a été construite dans le cadre du projet Mapuce, finalisé en 2015. **Danube décrit le parc immobilier de manière archétypale**, c'est-à-dire les principales tendances de dispositifs constructifs sont associées à des groupes des bâtiments aux caractéristiques similaires (les archétypes), en considérant les pratiques constructives et architecturales couramment employées en France métropolitaine. 

Cette base de données est utilisée pour des simulations de microclimat, notamment pour les calculs des températures en ville, puisque le parc immobilier contribue aux phénomènes d’îlot de chaleur. Danube décrivait les caractéristiques des bâtiments au moment de leur construction, sans tenir compte des rénovations successives qui ont pu avoir lieu. **La rénovation du parc immobilier modifie la dynamique des échanges thermiques entre les bâtiments et son l'environnement**, ce qui peut avoir un impact significatif sur les simulations microclimatiques. 

Ce travail consiste à **enrichir Danube en prenant en compte les rénovations** qui ont pu avoir lieu aux bâtiments representés par les archétypes Danube. Pour ce faire, les Diagnostiques de Performance Énergétique (DPE) disponibles dans la Base de Données Nationale des Bâtiments (BDNB) ont été utilisés. Dans un premier temps, un **mappage et filtrage des archétypes Danube** a été réalisé sur des données géolocalisées (_/preprocessing_data_). Ces **données géolocalisées** ont été le résultat d'une jointure spatiale de 4 jeux de données (ci-dessous) et ne peuvent être partagées pour des raisons de droits: 
- La carte de territoires Mapuce
- La BDNB v0.64 (version ayant droit aux fichier fonciers)
- Des cartes typologiques geoclimate (si possible)
- Filosofi v2015 produite par l'INSEE

Dans la suite, les **valeurs U des dispositifs Danube** ont été calculées avec la **méthode DPE 3CL 2012** en considérant la matérialité des archétypes Danube pour déterminer les seuils de la rénovation (_/data_analysis/danube_u_value_ranges_). Finalement, des **analyses statistiques** ont été appliqués pour étudier le **niveau de rénovation** des échantillons d'archétypes Danube (_/data_analysis/statistics_assembled_archetypes_). Cette analyse  s'est déroulée selon les étapes suivantes : 
- Des **statistiques descriptives** pour des valeur U des archétypes Danube accompagnées par ses plots de distributions avec les seuils utilisés pour déterminer la rénovation (_/analysis_density_distribution_). 
- L'étude de la **matérialité des archétypes** de chaque échantillon des données géolocalisés (_/resume_wall_roof_windows_)
- **Teste de Kolmogorov–Smirnov** pour déterminer si les échantillons avec une même U-valeur des dispositifs Danube appartenaient à la même distribution de probabilité (_/kolmogorov_smirnov_test_). 
- **Teste Chi² pour étudier la relation entre la rénovation des bâtiments et des indicateurs sociologiques**, taux de pauvreté et taux de proprietaires, de la base de données Filosofi (_/sociological_indicators_filosofi_).
