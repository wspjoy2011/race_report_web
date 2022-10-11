function closeAlert() {
  let alert = document.getElementById("alert_block");
  alert.style.display = "none";
  setTimeout(() => {
  console.log(window.location.replace("/"));
    }, 1000);
}
