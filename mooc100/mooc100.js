for (const d of document.getElementsByClassName("detail")) {
  for (const s of d.getElementsByClassName("s")) {
    s.lastElementChild.click()
  }
}
for (const d of document.getElementsByClassName("u-questionItem")) {
  for (const s of d.getElementsByTagName("textarea")) {
    s.value = "满分"
  }
}
