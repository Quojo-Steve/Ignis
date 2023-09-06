const slidePage = document.querySelector(".slidepage");
const firstNextBtn = document.querySelector(".nextBtn");
const prevBtnSec = document.querySelector(".prev-1");
const nextBtnSec = document.querySelector(".next-1");
const prevBtnThird = document.querySelector(".prev-2");
const nextBtnThird = document.querySelector(".next-2");
const prevBtnFourth = document.querySelector(".prev-3");
const submitBtn = document.querySelector(".submit");
const progressText = document.querySelectorAll(".step p");
const progressCheck = document.querySelectorAll(".step .check");
const bullet = document.querySelectorAll(".step .bullet");
const fname = document.querySelector(".fname");
const lname = document.querySelector(".lname");
const email = document.querySelector(".em");
const phone = document.querySelector(".pn");
const en = document.querySelector(".en");
const fireem = document.querySelector(".fireem");
const address = document.querySelector(".address");


let max = 4;
let current = 1;

firstNextBtn.addEventListener("click", (e) => {
  e.preventDefault();
  if (fname.value.trim() === "" && lname.value.trim() === "") {
    setTimeout(() => {
      alert("Please input your name");
    }, 800);
  } else {

    slidePage.style.marginLeft = "-25%";
    bullet[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    current += 1;
  }
});
nextBtnSec.addEventListener("click", (e) => {
  e.preventDefault();
  if (email.value.trim() === "" && phone.value.trim() === "") {
    setTimeout(() => {
      alert("Please input your email and phone number");
    }, 800);
  } else {
    slidePage.style.marginLeft = "-50%";
    bullet[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    current += 1;
  }
});
nextBtnThird.addEventListener("click", (e) => {
  e.preventDefault();
  if (address.value.trim() === "") {
    setTimeout(() => {
      alert("Please input your address");
    }, 800);
  } else {
  slidePage.style.marginLeft = "-75%";
  bullet[current - 1].classList.add("active");
  progressText[current - 1].classList.add("active");
  progressCheck[current - 1].classList.add("active");
  current += 1;
}
});
submitBtn.addEventListener("click", () => {
  if (en.value.trim() === "" && fireem.value.trim() === "") {
    setTimeout(() => {
      alert("Please input email and number");
    }, 800);
  } else {
    bullet[current - 1].classList.add("active");
    progressText[current - 1].classList.add("active");
    progressCheck[current - 1].classList.add("active");
    current += 1;
  }
});
prevBtnSec.addEventListener("click", (e) => {
  e.preventDefault();
  slidePage.style.marginLeft = "0%";
  bullet[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  current -= 1;
});
prevBtnThird.addEventListener("click", (e) => {
  e.preventDefault();
  slidePage.style.marginLeft = "-25%";
  bullet[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  current -= 1;
});
prevBtnFourth.addEventListener("click", (e) => {
  e.preventDefault();
  slidePage.style.marginLeft = "-50%";
  bullet[current - 2].classList.remove("active");
  progressText[current - 2].classList.remove("active");
  progressCheck[current - 2].classList.remove("active");
  current -= 1;
});
