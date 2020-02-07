flatpickr.localize(flatpickr.l10ns.es);
flatpickr('#valid-at', {
  enableTime: false,
  dateFormat: 'd/m/Y',
  minDate: '01/01/2018',
});

const form = document.querySelector('form');
const progressBar = document.querySelector('progress');
const resultContainer = document.getElementById('result-container');
const title = document.getElementById('form-title');
const goBackButton = document.getElementById('go-back-button');
const initialTitle = title.innerHTML;

form.addEventListener('submit', e => {
  e.preventDefault();
  form.hidden = true;
  calculatingTmcState();
  params = getFormData();
  getTmc(params);
});

goBackButton.onclick = () => {
  normalState();
};

function getFormData() {
  let elements = [...form.elements];
  elements = elements.filter(elem => {
    return elem.type !== 'radio' || (elem.type === 'radio' && elem.checked);
  });
  return new Map(elements.map(elem => [elem.name, elem.value]));
}

function calculatingTmcState() {
  progressBar.classList.remove('hide');
  title.innerHTML = 'Calculando tasa máxima convencional...';
}

function showTmcResultState(data) {
  progressBar.classList.add('hide');
  title.innerHTML = `Tasa máxima convencional: ${data.tmc}`;
  resultContainer.classList.remove('hide');
}

function normalState() {
  title.innerHTML = initialTitle;
  resultContainer.classList.add('hide');
  form.hidden = false;
}

function getTmc(params) {
  url_params = `credit-amount-uf=${params.get('credit-amount-uf')}&`;
  url_params =
    url_params + `credit-term-days=${params.get('credit-term-days')}&`;
  url_params = url_params + `valid-at=${params.get('valid-at')}&`;
  url_params = url_params + `operation-type=${params.get('operation-type')}`;
  fetch(`/api/v1/tmc/?${url_params}`, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: 'Api-Key SWvVO8RF.ZoqHc8jCYel6FIZPtqUiTieJ829fRAVn',
    },
  }).then(response => {
    response.json().then(data => {
      showTmcResultState(data);
    });
  });
}
