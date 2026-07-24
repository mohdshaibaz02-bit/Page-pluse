async function analyzeWebsite(){

    const url=document.getElementById("url").value;

    const result=document.getElementById("result");

    result.innerHTML="Loading...";

    try{

        const response=await fetch("http://127.0.0.1:5000/analyze",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                url:url
            })

        });

        const data=await response.json();

        if(data.error){

            result.innerHTML="<h3>"+data.error+"</h3>";

            return;

        }

        result.innerHTML=`

        <div class="card">

        <h2>Analysis Report</h2>

        <p><b>HTTP Status:</b> ${data.status}</p>

        <p><b>Response Time:</b> ${data.responseTime} ms</p>

        <p><b>Title:</b> ${data.title}</p>

        <p><b>Meta Description:</b> ${data.metaDescription}</p>

        <p><b>H1 Count:</b> ${data.h1Count}</p>

        <p><b>Images Missing Alt:</b> ${data.missingAltImages}</p>

        <p><b>Word Count:</b> ${data.wordCount}</p>

        </div>

        `;

    }

    catch(error){

        result.innerHTML="<h3>Unable to connect to backend.</h3>";

    }

}