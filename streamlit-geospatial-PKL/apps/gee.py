import ee
import streamlit as st
import geemap.foliumap as geemap


def Sentinel():

    st.header("Remote Sensing Classification (Sentinel Imagery)")

    row1_col1, row1_col2 = st.columns([3, 1])
    width = 950
    height = 600


    Map = geemap.Map()

    # Select the seven NLCD epoches after 2000.
    region = ["Kab. Bandung Barat", "Kab. Purwakarta"]

    # Get an NLCD image by year.
    def getRS(region):

        if region == "Kab. Bandung Barat":
            Map.set_center(lat=-6.920803423087094, lon=107.4476469379034, zoom=10)
            ee_path = 'users/bills/Bandung_Barat'
            west_bandung = ee.FeatureCollection(ee_path)
            west_bandung = west_bandung.geometry()

            # Clip the map
            sent2 = ee.ImageCollection(ee.ImageCollection('COPERNICUS/S2')
                                         .filterBounds(west_bandung)
                                         .filterDate('2021-01-01', '2021-11-01')
                                         .sort('CLOUD_COVERAGE_ASSESSMENT', False)).mosaic().clip(west_bandung)

            # Add the raster map
            rf_raster = ee.Image('users/bills/Bandung_Barat_RF')
            westBandung_raster = rf_raster.clip(west_bandung)
            
            # Add true color layer
            Map.addLayer(sent2, {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}, 'Bandung Barat')

            # Add the result of remote sensing classification map
            Map.addLayer(westBandung_raster, {'min': 0, 'max': 5,
                                              'palette': ['#d63000', '#98ff00', '#0b4a8b' ,'#188700', '#00beff', '#bf04c2']},
                                              'Bandung Barat (Random Forest)')
        
        elif region == "Kab. Purwakarta":
            Map.set_center(lat=-6.5425, lon=107.4377, zoom=10)
            path_ee = 'users/bills/Purwakarta'
            purwakarta = ee.FeatureCollection(path_ee)
            purwakarta = purwakarta.geometry()

            # Clip the map
            sent2 = ee.ImageCollection(ee.ImageCollection('COPERNICUS/S2_SR')
                                         .filterBounds(purwakarta)
                                         .filterDate('2021-01-01', '2021-11-01')
                                         .sort('CLOUD_COVERAGE_ASSESSMENT', False)).mosaic().clip(purwakarta)

            # Add the raster map
            raster_rf_purwakarta = ee.Image('users/bills/Purwakarta_RF')
            purwakarta_raster = raster_rf_purwakarta.clip(purwakarta)

            # Add true color layer
            Map.addLayer(sent2, {'min': 0, 'max': 3000, 'bands': ['B4', 'B3' ,'B2']}, 'Purwakarta')

            # Add the result of remote sensing classification map
            Map.addLayer(purwakarta_raster, {'min': 0, 'max': 5,
                                             'palette': ['#d63000', '#98ff00', '#0b4a8b' ,'#188700', '#00beff', '#bf04c2']},
                                             'Purwakarta (Random Forest)')
        
    def getLegend(region):
        if region == "Kab. Bandung Barat":
            legend_title = "Klasifikasi Lahan Kabupaten Bandung Barat"
            legend_dict = {
                'Awan': 'd63000',
                'Sawah': '98ff00',
                'Lahan Terbangun': '0b4a8b',
                'Hutan': '188700',
                'Badan Air': '00beff',
                'Lahan Kosong Non-Vegetatif': 'bf04c2'}
            Map.add_legend(legend_title=legend_title, legend_dict=legend_dict, layer_name='Kab. Bandung Barat')
        
        elif region == "Kab. Purwakarta":
            legend_title = "Klasifikasi Lahan Kabupaten Purwakarta"
            legend_dict = {
                'Awan': 'd63000',
                'Sawah': '98ff00',
                'Lahan Terbangun': '0b4a8b',
                'Hutan': '188700',
                'Badan Air': '00beff',
                'Lahan Kosong Non-Vegetatif': 'bf04c2'}
            Map.add_legend(legend_title=legend_title, legend_dict=legend_dict, layer_name='Kab. Purwakarta')

    with row1_col2:
        selected_region = st.multiselect("Select region", region)
        add_legend = st.checkbox("Show legend")

    if selected_region:
        for region in selected_region:
            getRS(region)

        if add_legend:
            getLegend(region)

        with row1_col1:
            Map.to_streamlit(width=width, height=height)
        
        st.subheader("Confusion Matrix")
        if region == "Kab. Bandung Barat":
            st.image("https://i.ibb.co/wryCW52/CM.png")
        else:
            st.image("https://i.ibb.co/J7VmJxx/CM-Purwakarta-Sent2.png")

    else:
        with row1_col1:
            Map.to_streamlit(width=width, height=height)

def Landsat():

    st.header("Remote Sensing Classification (Landsat Imagery)")

    row1_col1, row1_col2 = st.columns([3, 1])
    width = 950
    height = 600


    Map = geemap.Map()

    # Select the seven NLCD epoches after 2000.
    regions = ["Kab. Bandung Barat", "Kab. Purwakarta"]
    years = ["2013", "2021"]

    # Get an NLCD image by year.
    def getRS(region):

        if regions == "Kab. Bandung Barat":
            if years == "2013":
                Map.set_center(lat=-6.920803423087094, lon=107.4476469379034, zoom=10)
                ee_path = 'users/bills/Bandung_Barat'
                roi_BB = ee.FeatureCollection(ee_path)
                roi_BB = roi_BB.geometry()
                
                land8 = ee.ImageCollection(ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
                             .filterBounds(roi_BB)
                             .filterDate('2013-01-01', '2013-12-31')
                             .sort('CLOUD_COVER', False)).mosaic().clip(roi_BB)
                
                RF_past = ee.Image('users/bills/RF_Bandung_Barat_Past')
                RF_past = RF_past.clip(roi_BB)
                
                Map.addLayer(land8, {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}, 'Bandung Barat')
                
                Map.addLayer(RF_past, {'min':1, 'max': 6,
                                       'palette': ['#d63000', '#98ff00', '#0b4a8b' ,'#188700', '#00beff', '#bf04c2']},
                                       'Bandung Barat (Random Forest)')
            else:
                Map.set_center(lat=-6.920803423087094, lon=107.4476469379034, zoom=10)
                ee_path = 'users/bills/Bandung_Barat'
                west_bandung = ee.FeatureCollection(ee_path)
                west_bandung = west_bandung.geometry()

                # Clip the map
                land8 = ee.ImageCollection(ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
                             .filterDate('2021-01-01', '2021-11-01')
                             .filterBounds(west_bandung)
                             .sort('CLOUD_COVER', False)).mosaic().clip(west_bandung)

                # Add the raster map
                rf_raster = ee.Image('users/bills/Bandung_Barat_Land8_RF')
                westBandung_raster = rf_raster.clip(west_bandung)

                # Add true color layer
                Map.addLayer(land8, {'min': 0, 'max': 3000, 'bands': ['B4', 'B3', 'B2']}, 'Bandung Barat')

                # Add the result of remote sensing classification map
                Map.addLayer(westBandung_raster, {'min': 0, 'max': 5,
                                                  'palette': ['#d63000', '#98ff00', '#0b4a8b' ,'#188700', '#00beff', '#bf04c2']},
                                                  'Bandung Barat (Random Forest)')
        
        elif regions == "Kab. Purwakarta":
            Map.set_center(lat=-6.5425, lon=107.4377, zoom=10)
            path_ee = 'users/bills/Purwakarta'
            purwakarta = ee.FeatureCollection(path_ee)
            purwakarta = purwakarta.geometry()

            # Clip the map
            land8 = ee.ImageCollection(ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
                                         .filterBounds(purwakarta)
                                         .filterDate('2021-01-01', '2021-11-01')
                                         .sort('CLOUD_COVER', False)).mosaic().clip(purwakarta)

            # Add the raster map
            raster_rf_purwakarta = ee.Image('users/bills/Purwakarta_Land8_RF')
            purwakarta_raster = raster_rf_purwakarta.clip(purwakarta)

            # Add true color layer
            Map.addLayer(land8, {'min': 0, 'max': 3000, 'bands': ['B4', 'B3' ,'B2']}, 'Purwakarta')

            # Add the result of remote sensing classification map
            Map.addLayer(purwakarta_raster, {'min': 0, 'max': 5,
                                             'palette': ['#d63000', '#98ff00', '#0b4a8b' ,'#188700', '#00beff', '#bf04c2']},
                                             'Purwakarta (Random Forest)')

    def getLegend(region):
        if regions == "Kab. Bandung Barat":
            legend_title = "Klasifikasi Lahan Kabupaten Bandung Barat"
            legend_dict = {
                'Awan': 'd63000',
                'Sawah': '98ff00',
                'Lahan Terbangun': '0b4a8b',
                'Hutan': '188700',
                'Badan Air': '00beff',
                'Lahan Kosong Non-Vegetatif': 'bf04c2'}
            Map.add_legend(legend_title=legend_title, legend_dict=legend_dict, layer_name='Kab. Bandung Barat')
        
        elif regions == "Kab. Purwakarta":
            legend_title = "Klasifikasi Lahan Kabupaten Purwakarta"
            legend_dict = {
                'Awan': 'd63000',
                'Sawah': '98ff00',
                'Lahan Terbangun': '0b4a8b',
                'Hutan': '188700',
                'Badan Air': '00beff',
                'Lahan Kosong Non-Vegetatif': 'bf04c2'}
            Map.add_legend(legend_title=legend_title, legend_dict=legend_dict, layer_name='Kab. Purwakarta')

    with row1_col2:
        selected_region = st.multiselect("Select region", regions)
        selected_year = st.multiselect("Select year", years)
        add_legend = st.checkbox("Show legend")

    if selected_region:
        for region in selected_region:
            for year in selected_year:
                getRS(region)

        if add_legend:
            getLegend(region)

        with row1_col1:
            Map.to_streamlit(width=width, height=height)

    else:
        with row1_col1:
            Map.to_streamlit(width=width, height=height)

def app():
    st.title("Google Earth Engine Applications")

    apps = ["Sentinel Imagery", "Landsat Imagery"]

    selected_app = st.selectbox("Select an app", apps)

    if selected_app == "Sentinel Imagery":
        Sentinel()
    else:
        Landsat()
