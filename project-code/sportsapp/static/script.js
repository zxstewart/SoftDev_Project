function callGetFile(){
    console.log("test");
    //window.location.href += 'DAL_2018.csv';
    //window.location.href += filename;
    //using jquery to get data
    var filename_data = $('#fN').data("name");
    window.location.href += filename_data;
}