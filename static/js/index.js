const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

var url = location.search;
if (url.indexOf("register") !== -1) {
	container.classList.add("right-panel-active");
}else{
	container.classList.remove("right-panel-active");
}

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});
