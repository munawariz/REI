Morris.Area({
    element: 'siswa-chart',
    data: [{
        period: '2010',
        Pria: 50,
        Wanita: 80,
    }, {
        period: '2011',
        Pria: 130,
        Wanita: 100,
    }, {
        period: '2012',
        Pria: 80,
        Wanita: 60,
    }, {
        period: '2013',
        Pria: 70,
        Wanita: 200,
    }],
    xkey: 'period',
    ykeys: ['Pria', 'Wanita'],
    labels: ['Pria', 'Wanita'],
    pointSize: 3,
    fillOpacity: 0,
    pointStrokeColors:['#006DF0', '#933EC5'],
    behaveLikeLine: true,
    gridLineColor: '#e0e0e0',
    lineWidth: 1,
    hideHover: 'auto',
    lineColors: ['#006DF0', '#933EC5'],
    resize: true
    
});