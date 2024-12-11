import dask.dataframe as dd
import dotenv
import gc
import os
import pathlib
import plotly.express as px

# Load environment variables from .env file
dotenv.load_dotenv()

# Data source paths
MEMBERS_PATH_BASE = os.getenv('MEMBERS_PATH_BASE')
ENROLLMENT_PATH = os.getenv('ENROLLMENT_PATH')
SERVICES_PATH = os.getenv('SERVICES_PATH')

HTML_OUT_DIR = 'html_files'

def read_parquet_files(directory):
    try:
        ddf = dd.read_parquet(directory)
        return ddf
    except FileNotFoundError:
        print(f'Error: Directory "{directory}" not found.')
        return None
    except Exception as e:
        print(f'Error reading Parquet files: {e}')
        return None

def main():
    enrollment_ddf = read_parquet_files(ENROLLMENT_PATH)
    services_ddf = read_parquet_files(SERVICES_PATH)

    members_dirs = [p for p in pathlib.Path(MEMBERS_PATH_BASE).iterdir() if p.is_dir()]
    for members_dir in members_dirs:
        cohort = int(str(members_dir).split('/')[-1].split('_')[-1])

        members_ddf = read_parquet_files(members_dir)

        # Merge using dask.dataframe.merge
        merged_ddf = members_ddf.merge(enrollment_ddf, on='PRIMARY_PERSON_KEY', how='inner')
        merged_ddf = merged_ddf.merge(services_ddf, on='PRIMARY_PERSON_KEY', how='inner')

        # Handle missing values
        cols_to_check = ['MEM_RACE', 'MEM_ETHNICITY', 'MEM_GENDER', 'MEM_ZIP3','MEM_STATE', 'PROD_TYPE', 'SERVICE_SETTING', 'SERVICE_LINE', 'AMT_PAID', 'MEMBER_ID']
        for col in cols_to_check:
            if col in merged_ddf.columns:
                merged_ddf = merged_ddf.dropna(subset=[col])

        # Convert relevant columns to appropriate datatypes.  Handle 'N+' values in MEM_AGE
        for col in ['MEM_RACE', 'MEM_ETHNICITY']:
            if col in merged_ddf.columns:
                merged_ddf[col] = merged_ddf[col].astype(int)
        if 'MEM_AGE' in merged_ddf.columns:
            merged_ddf['MEM_AGE'] = merged_ddf['MEM_AGE'].astype(str).str.replace(r'(\d+)\+', lambda x: str(int(x.group(1)) + 1), regex=True).astype(int)

        # Race Mapping for better readability in plots
        race_mapping = {1: 'Asian', 2: 'Black', 3: 'Caucasian', 4: 'Other/Unknown'}
        if 'MEM_RACE' in merged_ddf.columns:
            merged_ddf['Race_Name'] = merged_ddf['MEM_RACE'].map(race_mapping, meta=('MEM_RACE', 'object'))

        # Geographic Disparities Visualization
        if 'MEM_STATE' in merged_ddf.columns and 'MEMBER_ID' in merged_ddf.columns:
            access_by_member_state = merged_ddf.groupby('MEM_STATE')['MEMBER_ID'].count().compute().reset_index()
            fig_member_access = px.choropleth(access_by_member_state, locations='MEM_STATE', locationmode='USA-states',
                                            scope='usa', color='MEMBER_ID', hover_data=['MEM_STATE', 'MEMBER_ID'],
                                            color_continuous_scale='Viridis', title='Healthcare Access by Member State')
            fig_member_access.write_html(f'{HTML_OUT_DIR}/member_access_by_state_{cohort}.html')

        # Racial Disparities Visualization
        if 'Race_Name' in merged_ddf.columns and 'SERVICE_LINE' in merged_ddf.columns:
            service_usage_by_race_ddf = merged_ddf[['Race_Name', 'SERVICE_LINE']]
            service_usage_by_race = service_usage_by_race_ddf.groupby('Race_Name')['SERVICE_LINE'].count().compute().reset_index()
            fig_service_usage = px.bar(service_usage_by_race, x='Race_Name', y='SERVICE_LINE',
                                    title='Service Usage by Race',
                                    labels={'Race_Name': 'Race', 'SERVICE_LINE': 'Number of Services'})
            fig_service_usage.write_html(f'{HTML_OUT_DIR}/service_usage_by_race_{cohort}.html')

        if 'Race_Name' in merged_ddf.columns and 'AMT_PAID' in merged_ddf.columns:
            cost_by_race_ddf = merged_ddf[['Race_Name', 'AMT_PAID']]
            cost_by_race = cost_by_race_ddf.groupby('Race_Name')['AMT_PAID'].sum().compute().reset_index()
            fig_cost_by_race = px.bar(cost_by_race, x='Race_Name', y='AMT_PAID',
                                    title='Total Cost by Race',
                                    labels={'Race_Name': 'Race', 'AMT_PAID': 'Total Amount Paid'})
            fig_cost_by_race.write_html(f'{HTML_OUT_DIR}/cost_by_race_{cohort}.html')

        # Gender Disparities Visualization
        if 'MEM_GENDER' in merged_ddf.columns and 'SERVICE_LINE' in merged_ddf.columns:
            service_usage_by_gender = merged_ddf.groupby('MEM_GENDER')['SERVICE_LINE'].count().compute().reset_index()
            fig_service_usage_gender = px.bar(service_usage_by_gender, x='MEM_GENDER', y='SERVICE_LINE',
                                            title='Service Usage by Gender',
                                            labels={'MEM_GENDER': 'Gender', 'SERVICE_LINE': 'Number of Services'})
            fig_service_usage_gender.write_html(f'{HTML_OUT_DIR}/service_usage_by_gender_{cohort}.html')

        # Age Disparities Visualization
        if 'MEM_AGE' in merged_ddf.columns and 'AMT_PAID' in merged_ddf.columns:
            cost_by_age = merged_ddf.groupby('MEM_AGE')['AMT_PAID'].sum().compute().reset_index()
            fig_cost_by_age = px.bar(cost_by_age, x='MEM_AGE', y='AMT_PAID',
                                    title='Total Cost by Age',
                                    labels={'MEM_AGE': 'Age', 'AMT_PAID': 'Total Amount Paid'})
            fig_cost_by_age.write_html(f'{HTML_OUT_DIR}/cost_by_age_{cohort}.html')

        # Ethnicity Disparities Visualization
        ethnicity_mapping = {1: 'Hispanic', 2: 'Non-Hispanic', 3: 'Unknown'}

        if 'MEM_ETHNICITY' in merged_ddf.columns:
            merged_ddf['Ethnicity_Name'] = merged_ddf['MEM_ETHNICITY'].map(ethnicity_mapping, meta=('MEM_ETHNICITY', 'object'))

        if 'Ethnicity_Name' in merged_ddf.columns and 'SERVICE_LINE' in merged_ddf.columns:
            service_usage_by_ethnicity = merged_ddf.groupby('Ethnicity_Name')['SERVICE_LINE'].count().compute().reset_index()
            fig_service_usage_ethnicity = px.bar(service_usage_by_ethnicity, x='Ethnicity_Name', y='SERVICE_LINE',
                                                title='Service Usage by Ethnicity',
                                                labels={'Ethnicity_Name': 'Ethnicity', 'SERVICE_LINE': 'Number of Services'})
            fig_service_usage_ethnicity.write_html(f'{HTML_OUT_DIR}/service_usage_by_ethnicity_{cohort}.html')

        if 'Ethnicity_Name' in merged_ddf.columns and 'AMT_PAID' in merged_ddf.columns:
            cost_by_ethnicity = merged_ddf.groupby('Ethnicity_Name')['AMT_PAID'].sum().compute().reset_index()
            fig_cost_by_ethnicity = px.bar(cost_by_ethnicity, x='Ethnicity_Name', y='AMT_PAID',
                                        title='Total Cost by Ethnicity',
                                        labels={'Ethnicity_Name': 'Ethnicity', 'AMT_PAID': 'Total Amount Paid'})
            fig_cost_by_ethnicity.write_html(f'{HTML_OUT_DIR}/cost_by_ethnicity_{cohort}.html')

        # Diagnosis Disparities Visualization

        if {'Race_Name', 'DIAG_CCS_1_LABEL', 'PRIMARY_PERSON_KEY', 'AMT_PAID'}.issubset(merged_ddf.columns):
            diagnosis_distribution = merged_ddf.groupby(['Race_Name', 'DIAG_CCS_1_LABEL'])['PRIMARY_PERSON_KEY'].count().compute().reset_index()
            diagnosis_codes = {label: i + 1 for i, label in enumerate(diagnosis_distribution['DIAG_CCS_1_LABEL'].unique())}
            diagnosis_distribution['Diagnosis_Code'] = diagnosis_distribution['DIAG_CCS_1_LABEL'].map(diagnosis_codes)

            # 1. Stacked Bar Chart: Diagnosis Distribution by Race
            fig_diagnosis_distribution = px.bar(diagnosis_distribution, x='Race_Name', y='PRIMARY_PERSON_KEY', color='DIAG_CCS_1_LABEL',
                                                barmode='stack', title='Diagnosis Distribution by Race',
                                                labels={'Race_Name': 'Race', 'PRIMARY_PERSON_KEY': 'Count', 'DIAG_CCS_1_LABEL': 'Diagnosis'},
                                                text='Diagnosis_Code', custom_data=['Diagnosis_Code', 'DIAG_CCS_1_LABEL'])
            fig_diagnosis_distribution.update_traces(textposition='inside', textfont_size=10)
            fig_diagnosis_distribution.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
            new_names = [f'{code} - {label}' for code, label in diagnosis_codes.items()]
            for i, name in enumerate(new_names):
                fig_diagnosis_distribution.data[i].name = name
            fig_diagnosis_distribution.update_traces(hovertemplate='Diagnosis Code: %{customdata[0]}<br>Diagnosis: %{customdata[1]}<br>Count: %{y}<extra></extra>')
            fig_diagnosis_distribution.write_html(f'{HTML_OUT_DIR}/diagnosis_distribution_{cohort}.html')

            # 2. Grouped Bar Chart: Average Cost by Diagnosis and Race
            avg_cost_by_diagnosis = merged_ddf.groupby(['DIAG_CCS_1_LABEL', 'Race_Name'])['AMT_PAID'].mean().compute().reset_index()
            avg_cost_by_diagnosis['Diagnosis_Code'] = avg_cost_by_diagnosis['DIAG_CCS_1_LABEL'].map(diagnosis_codes)
            fig_avg_cost_by_diagnosis = px.bar(avg_cost_by_diagnosis, x='DIAG_CCS_1_LABEL', y='AMT_PAID', color='Race_Name',
                                               barmode='group', title='Average Cost by Diagnosis and Race',
                                               labels={'DIAG_CCS_1_LABEL': 'Diagnosis', 'AMT_PAID': 'Average Cost', 'Race_Name': 'Race'},
                                               custom_data=['Diagnosis_Code', 'DIAG_CCS_1_LABEL'])
            fig_avg_cost_by_diagnosis.update_traces(textposition='inside', textfont_size=10)
            fig_avg_cost_by_diagnosis.update_traces(hovertemplate='Diagnosis Code: %{customdata[0]}<br>Diagnosis: %{customdata[1]}<br>Average Cost: %{y}<extra></extra>')
            fig_avg_cost_by_diagnosis.write_html(f'{HTML_OUT_DIR}/avg_cost_by_diagnosis_{cohort}.html')

            # 3. Heatmap: Number of Unique Individuals Diagnosed by Race and Diagnosis
            diagnosis_counts = merged_ddf.groupby(['Race_Name', 'DIAG_CCS_1_LABEL'])['PRIMARY_PERSON_KEY'].nunique().compute().unstack()

            fig_diagnosis_heatmap = px.imshow(diagnosis_counts,
                                              labels=dict(x='Race', y='Diagnosis', color='Count of Unique Individuals'),
                                              title='Number of Unique Individuals Diagnosed by Race and Diagnosis',
                                              color_continuous_scale='Viridis',
                                              x=diagnosis_counts.columns,
                                              y=diagnosis_counts.index)

            fig_diagnosis_heatmap.update_traces(hovertemplate='Race: %{y}<br>Diagnosis: %{x}<br>Count: %{z}<extra></extra>')

            fig_diagnosis_heatmap.write_html(f'{HTML_OUT_DIR}/diagnosis_heatmap_{cohort}.html')

            del merged_ddf
            del diagnosis_distribution
            del fig_diagnosis_distribution
            del avg_cost_by_diagnosis
            del fig_avg_cost_by_diagnosis
            gc.collect()

if __name__ == '__main__':
    main()
    print('done')
