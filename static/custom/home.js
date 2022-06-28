$(document).ready(function () {
    	$.ajaxSetup({
       headers: {
         "X-CSRFToken": $('[name=csrfmiddlewaretoken]').val()
       }
   });
   getSchoolStats();
   getStudentData();
   getClassData();
   getFeeBalances();
   getFeepayments();
   searchTerm();
   searchYear();
    searchClass();
    termChange();
    yearChange();
    classChange();
    examChange();
    subjectChange();




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

 function searchSubjects(id) {

        $('#subject_frm').select2({
            placeholder: 'Subjects',
            allowClear: true,
            width: '67%',
            ajax: {
                delay: 250,
                url: 'searchsubjects/'+id,
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function subjectChange() {

    $('#subject_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#subjectCode').val(data.id);
        getExamChart()

    });
    $("#subject_frm").on("select2:unselecting", function(e) {
    $('#subjectCode').val('')
 });

}

function searchTerm() {

        $('#term_frm').select2({
            placeholder: 'Term',
            allowClear: true,
            width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamterm',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}

function termChange() {
    $('#term_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#termCode').val(data.id);
        if($('#yearCode').val()!==''){
            $('#reg_frm').empty()
            $('#regCode').val('')
            console.log('year code '+$('#yearCode').val())
            console.log('term code '+data.id)
            searchExam(data.id,$('#yearCode').val());
        }
    });
    $("#term_frm").on("select2:unselecting", function(e) {
    $('#termCode').val('')
    $('#termName').val('')

 });
}

function searchYear() {
        $('#year_frm').select2({
            placeholder: 'Year',
            allowClear: true,
            width: '66%',
            ajax: {
                delay: 250,
                url: 'searchexamyear',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}

function yearChange() {
    $('#year_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#yearCode').val(data.id)

    });
    $("#year_frm").on("select2:unselecting", function(e) {
    $('#yearCode').val('')
    $('#yearName').val('')

 });
}

function searchClass() {
        $('#class_frm').select2({
            placeholder: 'Select Class',
            allowClear: true,
             width: '67%',
            ajax: {
                delay: 250,
                url: 'searchclasses',
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })

}
function classChange() {
    $('#class_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#classCode').val(data.id)
        searchSubjects($('#classCode').val())
    });
    $("#class_frm").on("select2:unselecting", function(e) {
    $('#classCode').val('')
 });
}
function searchExam(term,year) {
       $('#reg_frm').select2({
            placeholder: 'Exam',
            allowClear: true,
            width: '67%',

            ajax: {
                delay: 250,
                url: 'searchexamregister/'+term+'/'+year,
                data: function (params) {
                    console.log("AA", params);
                    return {
                        query: params.term,
                        gotoPage: params.page
                    }
                },

                processResults: function (data, params) {
                    params.page = params.page || 1;
                    console.log('data: ', data);
                    return {
                        results: data.results
                    };
                }

            }
        })
}
function examChange() {
    $('#reg_frm').on('select2:select', function (e) {
        var data = e.params.data;
        $('#regCode').val(data.id)
    });
    $("#reg_frm").on("select2:unselecting", function(e) {
    $('#regCode').val('')

 });
}
function getExamChart() {
    var examCode = $('#regCode').val();
    var classCode = $('#classCode').val();
    var subjectCode = $('#subjectCode').val();
    if (examCode === '' || classCode === '' || subjectCode === '') {
 swal({
                title: 'Alert!',
                type: 'info',
                text: 'Exam,Class and Subject are Mandatory to view perfomance!',
                confirmButtonText: 'OK'
            })
    } else {
        $.ajax({
            type: 'GET',
            url: 'examchartdata',
            data:{
                examCode: examCode,
                classCode: classCode,
                subjectCode: subjectCode
            }

        }).done(function (s) {
            if(s.length!==0) {
                createexamChart(s[0], s[1], s[2], s[3])
            }else{
                createexamChart([], [], [], [])
                bootbox.alert("No examination data exists for this exam on this class or subject!")
            }
        }).fail(function (xhr, error) {

        });

    }
}

function createexamChart(grades,students,colors, backgrounds) {
$('#canvasContainer').empty();
var canvas = document.createElement('canvas');
canvas.width=400;
canvas.height=400;
canvas.id='examChart';
$('#canvasContainer').append(canvas);

const ctx = document.getElementById('examChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: grades,
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
    }
});

}