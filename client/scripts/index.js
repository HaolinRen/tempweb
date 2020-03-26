
$(document).ready(function() {
	var checkOrder = -1;
	var selected = ''
	let selectDict = {}

	$('#submit').on('click', function() {
		let name = $('#nameinput').val()
		let id = $('#idinput').val()
		if (name == '') {
			alert('姓名不能为空！')
		} else if (id == '') {
			alert('姓名不能为空！')
		} else if (checkOrder == -1) {
			alert('请做出选择！')
		} else {

			$('#submitPane').addClass('loading');
			setTimeout(function() {
				$('#submitPane').removeClass('loading');
				
				let para = {
					'name': name,
					'id': id,
					'select': selected
				}
				linker.postData('/submit', para, d=>{

					if (d == '0') {
						alert('No such Person found from database, please check input!')
					} else {

						let submitres = $('#subres')
						if (d.category == 'a') {
							submitres.html('')
						} else {
							let info = '<p>根据你在事前问卷中选择的朋友名单，你的大多数朋友选择了区间<b>*</b>为未来一周沪深300指数的涨跌幅区间。</p>'
							let re = ''
							if (d.category == 'c') {
								let k = parseInt(Math.random() * Object.keys(selectDict).length)
								while (k == checkOrder) {
									k = parseInt(Math.random() * Object.keys(selectDict).length)
								}
								re = selectDict[k];
							} else {
								re = d.data
							}
							info = info.replace('*', re);
							submitres.html(info)
						} 
					}
				})
				$('.modal').modal({
					onDeny: function(){
				    	return true;
				    },
				    onApprove: function() {
				    	return true
				    }
				}).modal('show');
			}, 1000)
			
		}
	})

	var linker = {
		postData: function(path, data, callback) {
			$.ajax({
		        async: 'true',
		        type: 'POST',
		        url: path,
		        contentType: 'application/json',
		        data: JSON.stringify(data),
		        success: function (resData) {
		          callback(resData);
		        },
		        error: function (resData) {
		          console.log(resData.statusText);
		        }
		    })
		},
		getData: function(path, callback) {
			$.ajax({
				async: 'true',
		        type: 'GET',
		        url: path,
		        success: function (resData) {
		          callback(resData);
		        },
		        error: function (resData) {
		          console.log(resData.statusText);
		        }
			})
		}
	}

	function initCheckbox(ckbs, callback) {
		for (let k = 0; k < ckbs.length; k += 1) {
			ckbs.eq(k).checkbox({
				onChecked: function() {
					for (let j = 0; j < ckbs.length; j += 1) {
						if (j !== k) {
							ckbs.eq(j).checkbox('uncheck');
						}
					}
					checkOrder = k;
					if (callback) {
						callback(k)
					}
				},
				uncheckable: false
			})
		}
	}

	function createList(price) {
        let tableEle = $('#ptable');
        let textEle = '';
        let count = 0
        for (let i = -6; i < 6; i += 1) {
        	let p0 = (i * 0.01 + 1) * price
        	let p1 = ((i+1) * 0.01 + 1) * price

        	textEle += '<tr class="center aligned"><td class="collapsing"><div class="ui fitted radio checkbox"><input type="checkbox"> <label></label></div></td>'
        	if (i == -6) {
        		textEle += ' <td>(-∞, ' + (i+1) + '%)</td>'
            	textEle += '<td>(-∞, ' + p1.toFixed(2) + ')</td>'
            	selectDict[count] = '[-∞, ' + p1 + ']'
        	} else if (i == 5) {
        		textEle += ' <td>[' + i + '%, -∞)</td>'
            	textEle += '<td>[' + p0.toFixed(2) + ', -∞)</td>'
            	selectDict[count] = '[' + p0 + ', -∞]'
        	} else {
        		textEle += ' <td>[' + i + '%, ' + (i+1) + '%)</td>'
            	textEle += '<td>[' + p0.toFixed(2) + ', ' + p1.toFixed(2) + ')</td>'
            	selectDict[count] = '[' + p0 + ',' + p1 + ']'
        	}
        	count += 1;
            textEle += '</tr>'
        }

        tableEle.html(textEle)
        initCheckbox(tableEle.find('.checkbox'), select=>{
        	selected = selectDict[select];
        })
	}

	function initPage() {
		linker.getData('time', d=>{
			$('#date0').html(d.yesterday);
			$('.date1').html(d.nextMonday)
			$('.date2').html(d.nextSunday)
			createList(parseFloat(d.price))
		})
	}

	initPage()
});

