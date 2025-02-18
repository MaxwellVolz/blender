

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Resources

Download *sf_building_footprints.csv* and put in **sf/resources**

[Data SF: Building Footprints](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Building-Footprints/ynuv-fyni/data)
[Data SF: About Building Footprints Dataset](https://data.sfgov.org/Geographic-Locations-and-Boundaries/Building-Footprints/ynuv-fyni/about_data)


## Current Wacky Scaling

The Issue: 

Polygon information is GPS Based: 

```
 MULTIPOLYGON (((-122.42410005 37.76331376, -122.424099408 37.76329658,
```
and building height options are as follows

| variable        | description                                                                                        | units                         |
| --------------- | -------------------------------------------------------------------------------------------------- | ----------------------------- |
| gnd_cells50cm   | zonal stat: LiDAR-derived ground surface grid, pop of 50cm square cells sampled in building's zone | integer NAVD 1988 centimeters |
| p2010_zmaxn88ft | Input building mass (of 2010) min Z vertex elevation,                                              | NAVD 1988 ft                  |
| p2010_zmaxn88ft | Input building mass (of 2010) maximum Z vertex elevation,                                          | NAVD 1988 ft                  |


1. Import Blender
   1. Forward Axis: Y
   2. Up Axis: Z
2. Select All with **A**
   1. Scale By 5000,5000,0.00005



|                 |     |
| --------------- | --- |
| sf16_bldgid     |
| area_id         |
| mblr            |
| p2010_name      |
| p2010_zminn88ft |
| p2010_zmaxn88ft |
| gnd_cells50cm   |
| gnd_mincm       |
| gnd_maxcm       |
| gnd_rangecm     |
| gnd_meancm      |
| gnd_stdcm       |
| gnd_varietycm   |
| gnd_majoritycm  |
| gnd_minoritycm  |
| gnd_mediancm    |
| cells50cm_1st   |
| mincm_1st       |
| maxcm_1st       |
| rangecm_1st     |
| meancm_1st      |
| stdcm_1st       |
| varietycm_1st   |
| majoritycm_1st  |
| minoritycm_1st  |
| mediancm_1st    |
| hgt_cells50cm   |
| hgt_mincm       |
| hgt_maxcm       |
| hgt_rangecm     |
| hgt_meancm      |
| hgt_stdcm       |
| hgt_varietycm   |
| hgt_majoritycm  |
| hgt_minoritycm  |
| hgt_mediancm    |
| gnd_min_m       |
| median_1st_m    |
| hgt_median_m    |
| gnd1st_delta    |
| peak_1st_m      |
| globalid        |
| shape           |
| data_as_of      |
| data_loaded_at  |
201006.0022466
22466
SF3567011
SanfranE_0186.flt
59.816299999999998
98.996700000000004
827
1833
1900
67
1871.6444981899999
13.770246500000001
68
1879
1833
1872
827
2093
3073
980
2948.58041112
171.59816888
261
3036
2093
3021
827
218
1196
978
1076.95163241
168.64448580999999
249
1145
218
1144
18.329999999999998
30.210000000000001
11.44
11.880000000000001
30.73
{C8580986-B164-4379-A566-943DCDB9E456},"MULTIPOLYGON (((-122.42410005 37.76331376, -122.424099408 37.76329658, -122.42410442 37.763291486, -122.424106377 37.763289497, -122.424103855 37.763269227, -122.424096 37.76326382, -122.424093063 37.763254779, -122.424095123 37.763243248, -122.424100368 37.763238215, -122.424101757 37.763236881, -122.424107925 37.763232942, -122.424112889 37.763231011, -122.424120408 37.763230604, -122.424126881 37.763231481, -122.424133544 37.763232788, -122.424139571 37.763236022, -122.424164048 37.763234334, -122.424168809 37.763229412, -122.424170252 37.763227919, -122.424195064 37.763226487, -122.424203186 37.763232152, -122.424211769 37.763231757, -122.424214247 37.763229184, -122.42422475 37.763228755, -122.424224975 37.76322857, -122.424230053 37.763224369, -122.424251692 37.763223502, -122.424260754 37.763228651, -122.424272219 37.763228452, -122.424279679 37.763221506, -122.424303567 37.763221096, -122.424312289 37.763225492, -122.424352806 37.76322348, -122.424357585 37.76328402, -122.424327349 37.763285525, -122.424329258 37.763309669, -122.424280834 37.763312083, -122.424280215 37.763304235, -122.424233717 37.763306416, -122.424234761 37.763315508, -122.424108606 37.763321599, -122.42410005 37.76331376)))"
2023/09/11 12:00:00 PM
2025/02/15 10:13:51 AM