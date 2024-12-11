from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve the HTML files directory
app.mount("/html_files", StaticFiles(directory="./html_files"), name="html_files")

# Return HTML with embedded iframes
@app.get("/", response_class=HTMLResponse)
def read_root():
    dropdown = ''.join([f'<option value="{i}">Cohort {i}</option>' for i in range(1, 11)])

    preload_links = ''.join([
        f'<link rel="preload" href="/html_files/member_access_by_state_{i}.html" as="document">'
        f'<link rel="preload" href="/html_files/service_usage_by_race_{i}.html" as="document">'
        f'<link rel="preload" href="/html_files/cost_by_race_{i}.html" as="document">'
        f'<link rel="preload" href="/html_files/service_usage_by_gender_{i}.html" as="document">'
        f'<link rel="preload" href="/html_files/cost_by_age_{i}.html" as="document">' for i in range(1, 11)
    ])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Health Equity Explorer</title>
        {preload_links}
        <style>
            .dropdown-container {{
                margin-bottom: 10px;  /* Small gap between dropdowns */
            }}
            .button-container {{
                margin: 20px 0; /* Margin around the button */
            }}
            .button-group {{
                margin-left: 30px;
                display: inline-block;
            }}
            .expand-button {{
                background-color: #ddd; /* Light gray background for expand button */
                border: 1px solid #bbb;
            }}
            .new-tab-button {{
                background-color: #ccf; /* Light blue background for new tab buttons */
                border: 1px solid #99f;
            }}
        </style>
    </head>
    <body>
        <div style="display: flex; align-items: baseline;">
            <h3 style="margin: 0;">Select Cohorts to View Service and Cost Visualizations</h3>

            <span style="font-size: 90%; margin-left: 15px; line-height: 1.4;">
                &#8226; Each cohort is a population of 100,000 except the 10th cohort which is 7,464.
                The total population of the dataset is thus 907,464. &#8226;
            </span>
        </div>

        <div class="button-container">
            <button class="expand-button" onclick="expandAll()">Expand all</button>
            <div class="button-group">
                <button class="new-tab-button" onclick="openDiagnosisDistributions()">Diagnosis Distributions</button>
                <button class="new-tab-button" onclick="openDiagnosisCosts()">Diagnosis Costs</button>
                <button class="new-tab-button" onclick="openIndividualsDiagnosed()">Individuals Diagnosed</button>
                <button class="new-tab-button" onclick="openEthnicityComparisons()">Ethnicity Comparisons</button>
                <button class="new-tab-button" onclick="openProviderAvailability()">Provider Availability</button>
            </div>
        </div>

        {"".join([
            f'''
            <div class="dropdown-container">
                <label for="dropdown{i}">Cohort:</label>
                <select id="dropdown{i}" onchange="updateIframes({i})">
                    <option value="">Select Cohort</option>
                    {dropdown}
                </select>
            </div>
            <div id="cohort{i}_iframes" style="display: none; margin-top: 20px;">
                <div style="display: flex; justify-content: space-between;">
                    <iframe id="iframe{i}_1" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                    <iframe id="iframe{i}_2" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                    <iframe id="iframe{i}_3" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                    <iframe id="iframe{i}_4" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                    <iframe id="iframe{i}_5" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                </div>
            </div>
            '''
            for i in range(1, 11)
        ])}

        <script>
            function updateIframes(cohortNumber) {{
                const cohort = document.getElementById('dropdown' + cohortNumber).value;
                const iframeContainer = document.getElementById('cohort' + cohortNumber + '_iframes');

                if (!cohort) {{
                    iframeContainer.style.display = 'none';  // Hide iframe container
                    document.getElementById('iframe' + cohortNumber + '_1').src = '';
                    document.getElementById('iframe' + cohortNumber + '_2').src = '';
                    document.getElementById('iframe' + cohortNumber + '_3').src = '';
                    document.getElementById('iframe' + cohortNumber + '_4').src = '';
                    document.getElementById('iframe' + cohortNumber + '_5').src = '';
                    return;
                }}

                iframeContainer.style.display = 'block';  // Show iframe container
                document.getElementById('iframe' + cohortNumber + '_1').src = `/html_files/member_access_by_state_${{cohort}}.html`;
                document.getElementById('iframe' + cohortNumber + '_2').src = `/html_files/service_usage_by_race_${{cohort}}.html`;
                document.getElementById('iframe' + cohortNumber + '_3').src = `/html_files/cost_by_race_${{cohort}}.html`;
                document.getElementById('iframe' + cohortNumber + '_4').src = `/html_files/service_usage_by_gender_${{cohort}}.html`;
                document.getElementById('iframe' + cohortNumber + '_5').src = `/html_files/cost_by_age_${{cohort}}.html`;
            }}

            function expandAll() {{
                for (let i = 1; i <= 10; i++) {{
                    const dropdown = document.getElementById('dropdown' + i);
                    dropdown.value = i;  // Select cohort in dropdown
                    updateIframes(i);  // Trigger the iframe update for the selected cohort
                }}
            }}

            function openDiagnosisDistributions() {{
                const newWindow = window.open('', '_blank');
                newWindow.document.open();
                const dropdown = ''.concat(...Array.from({{length: 10}}, (_, i) => `<option value="${{i + 1}}">Cohort ${{i + 1}}</option>`));
                const preload_links = ''.concat(...Array.from({{length: 10}}, (_, i) => `
                    <link rel="preload" href="/html_files/member_access_by_state_${{i + 1}}.html" as="document">
                    <link rel="preload" href="/html_files/diagnosis_distribution_${{i + 1}}.html" as="document">
                `));
                const iframeRows = ''.concat(...Array.from({{length: 10}}, (_, i) => `
                    <div class="dropdown-container">
                        <label for="dropdown${{i + 1}}">Cohort:</label>
                        <select id="dropdown${{i + 1}}" onchange="updateIframes(${{i + 1}})">
                            <option value="">Select Cohort</option>
                            ${{dropdown}}
                        </select>
                    </div>
                    <div id="cohort${{i + 1}}_iframes" style="display: none; margin-top: 20px;">
                        <div style="display: flex; justify-content: space-between;">
                            <iframe id="iframe${{i + 1}}_1" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                            <iframe id="iframe${{i + 1}}_2" width="80%" height="750px" frameborder="0" loading="lazy"></iframe>
                        </div>
                    </div>
                `));
                const html = `<!DOCTYPE html>
                <html>
                <head>
                    <title>Diagnosis Distributions</title>
                    ${{preload_links}}
                    <style>
                        .dropdown-container {{ margin-bottom: 10px; }}
                        .button-container {{ margin: 20px 0; }}
                    </style>
                </head>
                <body>
                    <div style="display: flex; align-items: baseline;">
                        <h3 style="margin: 0;">Select Cohorts to View Diagnosis Distributionss</h3>

                        <span style="font-size: 90%; margin-left: 15px; line-height: 1.4;">
                            &#8226; Each cohort is a population of 100,000 except the 10th cohort which is 7,464.
                            The total population of the dataset is thus 907,464. &#8226;
                        </span>
                    </div>

                    <div class="button-container">
                        <button onclick="expandAll()">Expand all</button>
                    </div>
                    ${{iframeRows}}
                </body>
                </html>`;
                newWindow.document.write(html);

                // Create script element dynamically
                const script = newWindow.document.createElement('script');
                script.textContent = `
                    function updateIframes(cohortNumber) {{
                        const cohort = document.getElementById('dropdown' + cohortNumber).value;
                        const iframeContainer = document.getElementById('cohort' + cohortNumber + '_iframes');

                        if (!cohort) {{
                            iframeContainer.style.display = 'none';
                            document.getElementById('iframe' + cohortNumber + '_1').src = '';
                            document.getElementById('iframe' + cohortNumber + '_2').src = '';
                            return;
                        }}

                        iframeContainer.style.display = 'block';
                        document.getElementById('iframe' + cohortNumber + '_1').src = '/html_files/member_access_by_state_' + cohort + '.html';
                        document.getElementById('iframe' + cohortNumber + '_2').src = '/html_files/diagnosis_distribution_' + cohort + '.html';
                    }}

                    function expandAll() {{
                        for (let i = 1; i <= 10; i++) {{
                            const dropdown = document.getElementById('dropdown' + i);
                            dropdown.value = i;
                            updateIframes(i);
                        }}
                    }}
                `;
                newWindow.document.body.appendChild(script);

                newWindow.document.close();
            }}

            function openDiagnosisCosts() {{
                const newWindow = window.open('', '_blank');
                newWindow.document.open();
                const dropdown = ''.concat(...Array.from({{length: 10}}, (_, i) => `<option value="${{i + 1}}">Cohort ${{i + 1}}</option>`));
                const preload_links = ''.concat(...Array.from({{length: 10}}, (_, i) => `
                    <link rel="preload" href="/html_files/member_access_by_state_${{i + 1}}.html" as="document">
                    <link rel="preload" href="/html_files/avg_cost_by_diagnosis_${{i + 1}}.html" as="document">
                `));
                const iframeRows = ''.concat(...Array.from({{length: 10}}, (_, i) => `
                    <div class="dropdown-container">
                        <label for="dropdown${{i + 1}}">Cohort:</label>
                        <select id="dropdown${{i + 1}}" onchange="updateIframes(${{i + 1}})">
                            <option value="">Select Cohort</option>
                            ${{dropdown}}
                        </select>
                    </div>
                    <div id="cohort${{i + 1}}_iframes" style="display: none; margin-top: 20px;">
                        <div style="display: flex; justify-content: space-between;">
                            <iframe id="iframe${{i + 1}}_1" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                            <iframe id="iframe${{i + 1}}_2" width="80%" height="1000px" frameborder="0" loading="lazy"></iframe>
                        </div>
                    </div>
                `));
                const html = `<!DOCTYPE html>
                <html>
                <head>
                    <title>Diagnosis Costs</title>
                    ${{preload_links}}
                    <style>
                        .dropdown-container {{ margin-bottom: 10px; }}
                        .button-container {{ margin: 20px 0; }}
                    </style>
                </head>
                <body>
                    <div style="display: flex; align-items: baseline;">
                        <h3 style="margin: 0;">Select Cohorts to View Diagnosis Costss</h3>

                        <span style="font-size: 90%; margin-left: 15px; line-height: 1.4;">
                            &#8226; Each cohort is a population of 100,000 except the 10th cohort which is 7,464.
                            The total population of the dataset is thus 907,464. &#8226;
                        </span>
                    </div>

                    <div class="button-container">
                        <button onclick="expandAll()">Expand all</button>
                    </div>
                    ${{iframeRows}}
                </body>
                </html>`;
                newWindow.document.write(html);

                // Create script element dynamically
                const script = newWindow.document.createElement('script');
                script.textContent = `
                    function updateIframes(cohortNumber) {{
                        const cohort = document.getElementById('dropdown' + cohortNumber).value;
                        const iframeContainer = document.getElementById('cohort' + cohortNumber + '_iframes');

                        if (!cohort) {{
                            iframeContainer.style.display = 'none';
                            document.getElementById('iframe' + cohortNumber + '_1').src = '';
                            document.getElementById('iframe' + cohortNumber + '_2').src = '';
                            return;
                        }}

                        iframeContainer.style.display = 'block';
                        document.getElementById('iframe' + cohortNumber + '_1').src = '/html_files/member_access_by_state_' + cohort + '.html';
                        document.getElementById('iframe' + cohortNumber + '_2').src = '/html_files/avg_cost_by_diagnosis_' + cohort + '.html';
                    }}

                    function expandAll() {{
                        for (let i = 1; i <= 10; i++) {{
                            const dropdown = document.getElementById('dropdown' + i);
                            dropdown.value = i;
                            updateIframes(i);
                        }}
                    }}
                `;
                newWindow.document.body.appendChild(script);

                newWindow.document.close();
            }}

            function openIndividualsDiagnosed() {{
                const newWindow = window.open('', '_blank');
                newWindow.document.open();
                const dropdown = ''.concat(...Array.from({{length: 10}}, (_, i) => `<option value="${{i + 1}}">Cohort ${{i + 1}}</option>`));
                const preload_links = ''.concat(...Array.from({{length: 10}}, (_, i) => `
                    <link rel="preload" href="/html_files/member_access_by_state_${{i + 1}}.html" as="document">
                    <link rel="preload" href="/html_files/diagnosis_heatmap_${{i + 1}}.html" as="document">
                `));
                const iframeRows = ''.concat(...Array.from({{length: 10}}, (_, i) => `
                    <div class="dropdown-container">
                        <label for="dropdown${{i + 1}}">Cohort:</label>
                        <select id="dropdown${{i + 1}}" onchange="updateIframes(${{i + 1}})">
                            <option value="">Select Cohort</option>
                            ${{dropdown}}
                        </select>
                    </div>
                    <div id="cohort${{i + 1}}_iframes" style="display: none; margin-top: 20px;">
                        <div style="display: flex; justify-content: space-between;">
                            <iframe id="iframe${{i + 1}}_1" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                            <iframe id="iframe${{i + 1}}_2" width="80%" height="750px" frameborder="0" loading="lazy"></iframe>
                        </div>
                    </div>
                `));
                const html = `<!DOCTYPE html>
                <html>
                <head>
                    <title>Individuals Diagnosed</title>
                    ${{preload_links}}
                    <style>
                        .dropdown-container {{ margin-bottom: 10px; }}
                        .button-container {{ margin: 20px 0; }}
                    </style>
                </head>
                <body>
                    <div style="display: flex; align-items: baseline;">
                        <h3 style="margin: 0;">Select Cohorts to View Individuals Diagnosed</h3>

                        <span style="font-size: 90%; margin-left: 15px; line-height: 1.4;">
                            &#8226; Each cohort is a population of 100,000 except the 10th cohort which is 7,464.
                            The total population of the dataset is thus 907,464. &#8226;
                        </span>
                    </div>

                    <div class="button-container">
                        <button onclick="expandAll()">Expand all</button>
                    </div>
                    ${{iframeRows}}
                </body>
                </html>`;
                newWindow.document.write(html);

                // Create script element dynamically
                const script = newWindow.document.createElement('script');
                script.textContent = `
                    function updateIframes(cohortNumber) {{
                        const cohort = document.getElementById('dropdown' + cohortNumber).value;
                        const iframeContainer = document.getElementById('cohort' + cohortNumber + '_iframes');

                        if (!cohort) {{
                            iframeContainer.style.display = 'none';
                            document.getElementById('iframe' + cohortNumber + '_1').src = '';
                            document.getElementById('iframe' + cohortNumber + '_2').src = '';
                            return;
                        }}

                        iframeContainer.style.display = 'block';
                        document.getElementById('iframe' + cohortNumber + '_1').src = '/html_files/member_access_by_state_' + cohort + '.html';
                        document.getElementById('iframe' + cohortNumber + '_2').src = '/html_files/diagnosis_heatmap_' + cohort + '.html';
                    }}

                    function expandAll() {{
                        for (let i = 1; i <= 10; i++) {{
                            const dropdown = document.getElementById('dropdown' + i);
                            dropdown.value = i;
                            updateIframes(i);
                        }}
                    }}
                `;
                newWindow.document.body.appendChild(script);

                newWindow.document.close();
            }}

            function openEthnicityComparisons() {{
                const newWindow = window.open('', '_blank');
                newWindow.document.open();
                const dropdown = ''.concat(...Array.from({{length: 10}}, (_, i) => `<option value="${{i + 1}}">Cohort ${{i + 1}}</option>`));
                const preload_links = ''.concat(...Array.from({{length: 10}}, (_, i) => `
                    <link rel="preload" href="/html_files/member_access_by_state_${{i + 1}}.html" as="document">
                    <link rel="preload" href="/html_files/service_usage_by_ethnicity_${{i + 1}}.html" as="document">
                    <link rel="preload" href="/html_files/cost_by_ethnicity_${{i + 1}}.html" as="document">
                `));
                const iframeRows = ''.concat(...Array.from({{length: 10}}, (_, i) => `
                    <div class="dropdown-container">
                        <label for="dropdown${{i + 1}}">Cohort:</label>
                        <select id="dropdown${{i + 1}}" onchange="updateIframes(${{i + 1}})">
                            <option value="">Select Cohort</option>
                            ${{dropdown}}
                        </select>
                    </div>
                    <div id="cohort${{i + 1}}_iframes" style="display: none; margin-top: 20px;">
                        <div style="display: flex; justify-content: space-between;">
                            <iframe id="iframe${{i + 1}}_1" width="20%" height="500px" frameborder="0" loading="lazy"></iframe>
                            <iframe id="iframe${{i + 1}}_2" width="40%" height="500px" frameborder="0" loading="lazy"></iframe>
                            <iframe id="iframe${{i + 1}}_3" width="40%" height="500px" frameborder="0" loading="lazy"></iframe>
                        </div>
                    </div>
                `));
                const html = `<!DOCTYPE html>
                <html>
                <head>
                    <title>Ethnicity Comparisons</title>
                    ${{preload_links}}
                    <style>
                        .dropdown-container {{ margin-bottom: 10px; }}
                        .button-container {{ margin: 20px 0; }}
                    </style>
                </head>
                <body>
                    <div style="display: flex; align-items: baseline;">
                        <h3 style="margin: 0;">Select Cohorts to View Ethnicity Comparisons</h3>

                        <span style="font-size: 90%; margin-left: 15px; line-height: 1.4;">
                            &#8226; Each cohort is a population of 100,000 except the 10th cohort which is 7,464.
                            The total population of the dataset is thus 907,464. &#8226;
                        </span>
                    </div>

                    <div class="button-container">
                        <button onclick="expandAll()">Expand all</button>
                    </div>
                    ${{iframeRows}}
                </body>
                </html>`;
                newWindow.document.write(html);

                // Create script element dynamically
                const script = newWindow.document.createElement('script');
                script.textContent = `
                    function updateIframes(cohortNumber) {{
                        const cohort = document.getElementById('dropdown' + cohortNumber).value;
                        const iframeContainer = document.getElementById('cohort' + cohortNumber + '_iframes');

                        if (!cohort) {{
                            iframeContainer.style.display = 'none';
                            document.getElementById('iframe' + cohortNumber + '_1').src = '';
                            document.getElementById('iframe' + cohortNumber + '_2').src = '';
                            document.getElementById('iframe' + cohortNumber + '_3').src = '';
                            return;
                        }}

                        iframeContainer.style.display = 'block';
                        document.getElementById('iframe' + cohortNumber + '_1').src = '/html_files/member_access_by_state_' + cohort + '.html';
                        document.getElementById('iframe' + cohortNumber + '_2').src = '/html_files/service_usage_by_ethnicity_' + cohort + '.html';
                        document.getElementById('iframe' + cohortNumber + '_3').src = '/html_files/cost_by_ethnicity_' + cohort + '.html';
                    }}

                    function expandAll() {{
                        for (let i = 1; i <= 10; i++) {{
                            const dropdown = document.getElementById('dropdown' + i);
                            dropdown.value = i;
                            updateIframes(i);
                        }}
                    }}
                `;
                newWindow.document.body.appendChild(script);

                newWindow.document.close();
            }}

            function openProviderAvailability() {{
                const newWindow = window.open('', '_blank');
                newWindow.document.open();

                const iframeHtml = `
                    <iframe src="/html_files/provider_availability_by_state.html" width="90%" height="800px" frameborder="0"></iframe>
                `;

                const html = `<!DOCTYPE html>
                <html>
                <head>
                    <title>Provider Availability</title>
                </head>
                <body>
                    ${{iframeHtml}}
                </body>
                </html>`;

                newWindow.document.write(html);
                newWindow.document.close();
            }}

        </script>

        <div style="text-align: left; margin-top: 30px; font-size: 14px; color: #666;">
            Powered by data copyrighted by
            <a href="https://www.milliman.com" target="_blank" style="color: #007bff; text-decoration: none;">Milliman MedInsight</a>.
        </div>
    </body>
    </html>
    """

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
