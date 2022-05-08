window.onload = ()=>{
    var path = window.location.pathname;
    var session_id = path.split('/').slice(-1)[0];
    console.log(session_id);
    document.getElementById('start').onclick = ()=>{
        console.log('start');
        var url = `/session/run/${session_id}`
        console.log(url);
        fetch(url).then((res)=>{
            res.json().then((val)=>{
                console.log(val);
            })
        })
    }
    document.getElementById('stop').onclick = ()=>{
        console.log('stop');
    }
}