(async ()=> {
    const response = await axios.get('time');
    CountDownTimer(response.data.endtime, 'HourCountdown');
})();

function CountDownTimer(dt, id) {
    var end = new Date(dt);
    var _second = 1000;
    var _minute = _second * 60;
    var _hour = _minute * 60;
    var _day = _hour * 24;
    var timer;

    function showRemaining() {
        var now = new Date();
        var distance = end - now;
      // 시간 종료 시 뜨는 문구
        if (distance < 0) {
            clearInterval(timer);
            document.getElementById("HourCountdown").innerHTML = '카운트다운이 끝났습니다. 곧 결과를 공개합니다!';
            return
        }
    var days = Math.floor(distance / _day);
    var hours = Math.floor((distance % _day) / _hour);
    var minutes = Math.floor((distance % _hour) / _minute);
    var seconds = Math.floor((distance % _minute) / _second);
    document.getElementById(id).innerHTML = days + '일 ';
    document.getElementById(id).innerHTML += hours + '시간 ';
    document.getElementById(id).innerHTML += minutes + '분 ';
    document.getElementById(id).innerHTML += seconds + '초';
}
    timer = setInterval(showRemaining, 1000);
}