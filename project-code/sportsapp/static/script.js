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