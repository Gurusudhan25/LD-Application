function animate(obj, initVal, lastVal, duration) {
    let startTime = null;
    const step = (currentTime) => {
        if (!startTime) {
            startTime = currentTime;
        }
        const progress = Math.min((currentTime - startTime) / duration, 100);
        obj.innerHTML = Math.floor(progress * (lastVal - initVal) + initVal);
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            window.cancelAnimationFrame(window.requestAnimationFrame(step));
        }
    };
    window.requestAnimationFrame(step);
}

async function getData() {
    let students = await fetch("/studentsData");
    let data = await students.json();
    return data;
}

async function just() {
    let students = await getData();
    // const obj = document.getElementById("counter");
    animate(document.getElementById("0101"), 0, students, 1000);
    animate(document.getElementById("0102"), 0, 263, 7000);
    animate(document.getElementById("0103"), 0, 337, 7000);
}
just();
