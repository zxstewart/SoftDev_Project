function callGetFile(){
    console.log("test");
    //window.location.href += 'DAL_2018.csv';
    //window.location.href += filename;
    //using jquery to get data
    var filename_data = $('#fN').data("name");
    let str = window.location.href;
    //handles home page download data when the url is "/home"
    str = str.slice(0,-4);
    str += filename_data;
    location.replace(str);
}

function togglePlayerList(){
    let year_select = document.getElementById('yearBox');
    let team_select = document.getElementById('teamList');
    let player_select = document.getElementById('playList');
    let request_type = document.getElementById('sport_type');

    if(request_type.value == 'league_stats'){
        year_select.style.height = "0";
        year_select.style.visibility = "hidden";
        team_select.style.height="0";
        team_select.style.visibility="hidden";
        player_select.style.height="0";
        player_select.style.visibility="hidden";
    }
    if(request_type.value != 'league_stats'){
        year_select.style.height = "auto";
        year_select.style.visibility = "visible";
        team_select.style.height="auto";
        team_select.style.visibility="visible";
        player_select.style.height="0";
        player_select.style.visibility="hidden";
    }
}
