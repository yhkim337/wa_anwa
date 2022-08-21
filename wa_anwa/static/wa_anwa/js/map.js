
const checkbox = document.getElementById("submitbutton");

const wrap = document.querySelector('.wrap')
const items = document.querySelectorAll('.OUTLINE')
wrap.addEventListener('click', e => {
    const target = e.target
    if (target.classList.contains('OUTLINE')) {
        showbettingmodal(target.id)
    }
});

document.getElementById("bettingmodalclose").addEventListener("click", ()=>document.getElementById("modal").classList.remove("show"))


const showbettingmodal =  async (region) => {
    const response = await axios.get('time');
    const modal = document.getElementById("modal")
    modal.classList.add("show");
    document.getElementById("region-name").innerHTML = region
    document.getElementById("amorpm").innerHTML = `${response.data.hour}시`
};





const bettingSubmit = async () => {
    const region = document.getElementById("region-name").innerHTML
    const wa = document.getElementById("wa")
    const a = await axios.get('time');
    const data = new FormData();
    data.append("region", region);
    data.append("time", a.data.hour);
    data.append("date", a.data.date);
    data.append("choice", wa.checked);
    data.append("point", document.getElementById("pointselect").value);
    const response = await axios.post('createparticipate');
    document.getElementById(region).style.backgroundColor =  wa.checked ? "blue" : "black";
    const modal = document.getElementById("modal");
    modal.classList.remove("show");
};

const Ablesubmit = () => {
    checkbox.disabled = false;
};

const Disablesubmit = () => {
    checkbox.disabled = true;
};

(()=>{    
    document.getElementById('inputdiv').addEventListener("change", function (e) {
        if (document.getElementById("pointselect").value > 0 && document.querySelector('input[name="selectwaanwa"]:checked') !== null) {
            Ablesubmit();
        }
        if (Number.isInteger(document.getElementById("pointselect").value)) {
            Disablesubmit();
        }
    })
    document.getElementById("submitbutton").addEventListener("click", ()=>bettingSubmit())
})();

