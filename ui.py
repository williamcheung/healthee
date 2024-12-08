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
        f'<link rel="preload" href="/html_files/cost_by_race_{i}.html" as="document">' for i in range(1, 11)
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
        </style>
    </head>
    <body>
        <div style="display: flex; align-items: baseline;">
            <h3 style="margin: 0;">Select Cohorts to View Visualizations</h3>

            <span style="font-size: 90%; margin-left: 15px; line-height: 1.4;">
                &#8226; Each cohort is a population of 100,000 except the 10th cohort which is 7,464.
                The total population of the dataset is thus 907,464. &#8226;
            </span>
        </div>

        <div class="button-container">
            <button onclick="expandAll()">Expand all</button>
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
                    <iframe id="iframe{i}_1" width="33%" height="500px" frameborder="0" loading="lazy"></iframe>
                    <iframe id="iframe{i}_2" width="33%" height="500px" frameborder="0" loading="lazy"></iframe>
                    <iframe id="iframe{i}_3" width="33%" height="500px" frameborder="0" loading="lazy"></iframe>
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
                    return;
                }}

                iframeContainer.style.display = 'block';  // Show iframe container
                document.getElementById('iframe' + cohortNumber + '_1').src = `/html_files/member_access_by_state_${{cohort}}.html`;
                document.getElementById('iframe' + cohortNumber + '_2').src = `/html_files/service_usage_by_race_${{cohort}}.html`;
                document.getElementById('iframe' + cohortNumber + '_3').src = `/html_files/cost_by_race_${{cohort}}.html`;
            }}

            function expandAll() {{
                for (let i = 1; i <= 10; i++) {{
                    const dropdown = document.getElementById('dropdown' + i);
                    dropdown.value = i;  // Select cohort in dropdown
                    updateIframes(i);  // Trigger the iframe update for the selected cohort
                }}
            }}
        </script>
    </body>
    </html>
    """

# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
