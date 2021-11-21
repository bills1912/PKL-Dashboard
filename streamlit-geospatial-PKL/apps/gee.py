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
                                              'palette': ['#d6d6d6', '#fffd0e', '#d90ee1', '#40d808', '#276fff', '#c20000']},
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
                                             'palette': ['#ff9999', '#fbff95', '#9999ff' ,'#75bca4', '#99ffff', '#0c19ff']},
                                             'Purwakarta (Random Forest)')
        
    def getLegend(region):
        if region == "Kab. Bandung Barat":
            legend_title = "Klasifikasi Lahan Kabupaten Bandung Barat"
            legend_dict = {
                'Awan': 'd6d6d6',
                'Sawah': 'fffd0e',
                'Lahan Terbangun': 'd90ee1',
                'Hutan': '40d808',
                'Badan Air': '276fff',
                'Lahan Kosong Non-Vegetatif': 'c20000'}
            Map.add_legend(legend_title=legend_title, legend_dict=legend_dict, layer_name='Kab. Bandung Barat')
        
        elif region == "Kab. Purwakarta":
            legend_title = "Klasifikasi Lahan Kabupaten Purwakarta"
            legend_dict = {
                'Awan': 'ff9999',
                'Sawah': 'fbff95',
                'Lahan Terbangun': '9999ff',
                'Hutan': '75bca4',
                'Badan Air': '99ffff',
                'Lahan Kosong Non-Vegetatif': '0c19ff'}
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
            pass

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
    region = ["Kab. Bandung Barat", "Kab. Purwakarta"]

    # Get an NLCD image by year.
    def getRS(region):

        if region == "Kab. Bandung Barat":
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
                                              'palette': ['#ff0000', '#00ff00', '#ffe600', '#8c9900', '#009999', '#ff00ff']},
                                              'Bandung Barat (Random Forest)')
        
        elif region == "Kab. Purwakarta":
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
        if region == "Kab. Bandung Barat":
            legend_title = "Klasifikasi Lahan Kabupaten Bandung Barat"
            legend_dict = {
                'Awan': 'ff0000',
                'Sawah': '00ff00',
                'Lahan Terbangun': 'ffe600',
                'Hutan': '8c9900',
                'Badan Air': '009999',
                'Lahan Kosong Non-Vegetatif': 'ff00ff'}
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
