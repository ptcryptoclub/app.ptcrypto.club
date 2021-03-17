

function adminLastUpdate(){
    let apiSecret = document.getElementById("APISecret").value;
    fetch('/api/admin/live-data/'+ apiSecret +'/').then(
        function(response){
            response.json().then(
                function (data) {
                    for (let line of data) {
                        let element = document.getElementById(line['market']+ '-' + line['base']+ '-' + line['quote'])
                        element.innerHTML = "<td>"+ line['market'] +"</td><td>"+ line['base'].toUpperCase() +"</td><td>"+ line['quote'].toUpperCase() +"</td><td>"+ line['date'] +"</td>"
                        if (line['all_good']){
                            element.className = "text-success"
                        }
                        else {
                            element.className = "text-danger"
                        }
                    }
                }
            )
        }
    );
}