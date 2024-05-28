document.getElementById('submit-btn').addEventListener('click', parse_links);

function parse_links() {
    var nation = document.getElementById('nation-link').value;
    var profile = document.getElementById('forum-profile').value;

    var profileNumberMatch = profile.match(/profile\/(\d+)/);
    var profileNumber = profileNumberMatch ? profileNumberMatch[1] : 'Not found';

    var nationName = nation.split('nation=')[1] || '';
    nationName = nationName.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');

    n_hype = '=HYPERLINK(' + '"' + nation + '",' + '"' + nationName + '")'
    f_hype = '=HYPERLINK(' + '"' + profile + '",' + '"' + profileNumber + '")'

    document.getElementById('nation-hyper').innerHTML = n_hype;
    document.getElementById('profile-hyper').innerHTML = f_hype;
    document.getElementById('nation-hyper').style.color = 'green';
    document.getElementById('profile-hyper').style.color = 'green';
}
