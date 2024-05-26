document.getElementById('check-btn').addEventListener('click', check_nation);

function check_nation() {
    var nation = document.getElementById('nation').value;
    var url = "https://www.nationstates.net/cgi-bin/api.cgi?nation=" + encodeURIComponent(nation);
    var n_url = "https://www.nationstates.net/nation=";
    fetch(url)
    .then(response => {
        if (!response.ok) {
            if (response.status == 404) {
                throw new Error("Nation does not exist (404), please check for yourself: " + n_url + nation);
            } else {
                throw new Error("Could not send request due to a potential network error, try again.");
            }
        }
        return response.text();
    })
    .then(xmlString => {
        const parser = new DOMParser();
        const xmlDocument = parser.parseFromString(xmlString, 'text/xml');
        const name = xmlDocument.querySelector('NAME').textContent;
        const region = xmlDocument.querySelector('REGION').textContent;
        const unstatus = xmlDocument.querySelector('UNSTATUS').textContent;

        if (region !== 'The North Pacific') {
            document.getElementById('region-status').innerHTML = "Nation not in The North Pacific";
            document.getElementById('region-status').style.color = "red";
        } else {
            document.getElementById('region-status').innerHTML = "REGION: PASS";
            document.getElementById('region-status').style.color = "darkblue";
        }

        if (unstatus !== "WA Member" && unstatus !== 'WA Delegate') {
            document.getElementById('wa-status').innerHTML = "Nation not in WA";
            document.getElementById('wa-status').style.color = "coral";
        } else {
            document.getElementById('wa-status').innerHTML = "WA: PASS";
            document.getElementById('wa-status').style.color = "darkblue";
        }

        document.getElementById('nation').innerHTML = "Nation: " + name;
        document.getElementById('region').innerHTML = "Region: " + region;
        document.getElementById('wa').innerHTML = "WA Status: " + unstatus;
    })
    .catch(error => {
        console.error('Error:', error.message);
        document.getElementById('nation-status').innerHTML = "Error: " + error.message;
        document.getElementById('nation-status').style.color = "red";
    });
}