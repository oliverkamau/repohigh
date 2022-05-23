$(document).ready(function () {
    	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
   });
   getSchoolStats()
   getStudentData()
   getClassData()
   getFeeBalances()
   getFeepayments()

   })
   function getStudentData(){
    $.ajax({
        type: 'GET',
        url: 'genderdata',

    }).done(function (s) {
     creategenderChart(s);
    }).fail(function (xhr, error) {
    });
   }
 function getSchoolStats(){
    $.ajax({
        type: 'GET',
        url: 'getstats',

    }).done(function (s) {
    $('#total').text(s.total)
    $('#teachers').text(s.teachers)
    $('#inschool').text(s.inschool)
    $('#outofschool').text(s.outofschool)

    }).fail(function (xhr, error) {
    });
   }
    function getClassData(){
    $.ajax({
        type: 'GET',
        url: 'classdata',

    }).done(function (s) {
     createclassChart(s[0],s[1],s[2],s[3])
    }).fail(function (xhr, error) {
    });
   }
   function getFeeBalances(){
    $.ajax({
        type: 'GET',
        url: 'feebalances',

    }).done(function (s) {
     createfeeChart(s[0],s[1],s[2],s[3])
    }).fail(function (xhr, error) {
    });
   }
     function getFeepayments(){
    $.ajax({
        type: 'GET',
        url: 'paymentmodes',

    }).done(function (s) {
     createpaymentChart(s[0],s[1],s[2],s[3])
    }).fail(function (xhr, error) {
    });
   }

 function creategenderChart(data){

const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: ['Male', 'Female'],
        datasets: [{
            label: 'Gender Distribution',
            data: data,
            backgroundColor: [
//                "#455C73",
                 "#3498DB",
                "#9B59B6",
//                'rgba(255, 206, 86, 0.2)',
//                'rgba(75, 192, 192, 0.2)',
//                'rgba(153, 102, 255, 0.2)',
//                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
//                'rgba(255, 206, 86, 1)',
//                'rgba(75, 192, 192, 1)',
//                'rgba(153, 102, 255, 1)',
//                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
              responsive: true,

    }
});

 }


 function createclassChart(forms,students,colors, backgrounds){

const ctx = document.getElementById('classes').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: forms,
        datasets: [{
            label: 'Students Per Class',
            data: students,
            backgroundColor: colors,
            borderColor: backgrounds,
            borderWidth: 1
        }]
    },
    options: {
       responsive: true,
       indexAxis: 'y',
    }
});

 }

 function createfeeChart(forms,students,colors, backgrounds){

const ctx = document.getElementById('feeBalance').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: forms,
        datasets: [{
            label: 'Fee Balance Per Class',
            data: students,
            backgroundColor: colors,
            borderColor: backgrounds,
            borderWidth: 1
        }]
    },
    options: {
       responsive: true,
       indexAxis: 'y',
    }
});

 }

 function createpaymentChart(forms,students,colors, backgrounds){

const ctx = document.getElementById('paymentMode').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: forms,
        datasets: [{
            label: 'Fee Per Payment Mode',
            data: students,
            backgroundColor: colors,
            borderColor: backgrounds,
            borderWidth: 1
        }]
    },
    options: {
       responsive: true,
       indexAxis: 'x',
    }
});

 }