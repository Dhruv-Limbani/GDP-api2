base_url = "https://general-disease-pred-api.onrender.com/";
syms = ['cough','chills'];
base_route_for_likely_syms = "get_lksyms?"
base_route_for_prediction = "predict?"
custom_url = "";
for(let i=0; i<syms.length;i++)
{
    custom_url = custom_url.concat(`symptoms=${syms[i]}&`)
}
custom_url = base_route_for_prediction.concat(custom_url.substring(0,custom_url.length-1))
fetch(`https://general-disease-pred-api.onrender.com/${custom_url}`)
.then(Response => {
     return Response.json();
})
.then(users=>{
    console.log(users)
});