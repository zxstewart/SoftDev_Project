function callGetFile(filename_data){
    //using jquery to get data
    //let filename_data = $('#fN').data("name");
    let str = window.location.href;
    //determine if we are at '/' or '/home'
    if(str.endsWith('home')){
        //handles home page download data when the url is "/home"
        str = str.slice(0,-4);
        str += filename_data;
        location.replace(str);
    }
    else{
        str += filename_data;
        location.replace(str);
    }
}

function togglePlayerList(){
    let year_select = document.getElementById('yearBox');
    let team_select = document.getElementById('teamList');
    let player_select = document.getElementById('playList');
    let request_type = document.getElementById('sport_type');

    if(request_type.value == 'league_stats'){
        year_select.style.height = "auto";
        year_select.style.display = "block";
        team_select.style.height="0";
        team_select.style.display="none";
        player_select.style.height="0";
        player_select.style.display="none";
    }
    else if(request_type.value == 'season_schedule' || request_type.value == 'season_roster'){
        year_select.style.height = "auto";
        year_select.style.display = "block";
        team_select.style.height="auto";
        team_select.style.display="block";
        player_select.style.height="0";
        player_select.style.display="none";
    }
    else{
        year_select.style.height = "auto";
        year_select.style.display = "block";
        team_select.style.height="auto";
        team_select.style.display="block";
        player_select.style.height="auto";
        player_select.style.display="block";
    }
}

function displayTableData(filename_data){
    //call the viewtable route
    let str = window.location.href;
    //determine if we are at '/' or '/home'
    if(str.endsWith('home')){
        //handles home page download data when the url is "/home"
        str = str.slice(0,-4);
        str += 'viewData/';
        str += filename_data;
        location.replace(str);
    }
    else{
        str += 'viewData/';
        str += filename_data;
        location.replace(str);
    }
}