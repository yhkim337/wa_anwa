const a = (async () => {
    const response = await axios.get('wa_anwa/time');
    return response
  })()

function showbettingmodal(region) {
    bettingmodal = document.getElementById("bettingmodal");
    bettingmodal.classList.add("show");
    document.getElementById("region-name").innerHTML = region
    document.getElementById("8amor6pm").innerHTML = a.data.hour
}

const bettingsubmit = async () => {
    const data = new FormData();
    data.append("region", document.getElementById("region-name").innerHTML);
    data.append("time", a.data.hour);
    data.append("date", `${a.data.year}.${a.data.month}.${a.data.day}`);
    const response = await axios.post('wa_anwa/createparticipate');
    bettingmodal = document.getElementById("bettingmodal");
    bettingmodal.classList.remove("show");
}