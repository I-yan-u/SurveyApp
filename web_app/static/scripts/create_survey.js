$(document).ready(() => {

  // Banner slider
  $('.banner_left #survey_editor button').click(() => {
    $(".banner").animate({ height: '5vh' }, 1000);
    $(".banner_left").animate({ height: '0', opacity: 0 }, 1000);
    $(".banner_right").animate({ height: '0', opacity: 0 }, 1000);
    $('#show_how').animate({opacity: '1'}, 1000);
    $("#survey-title").trigger('focus');
  });

  $('#show_how').click(() => {
    $(".banner").animate({ height: '80vh' }, 1000);
    $(".banner_left").animate({height: '80vh', opacity: 1 }, 1000);
    $(".banner_right").animate({height: '80vh', opacity: 1 }, 1000);
    $('#show_how').animate({opacity: '0'}, 1000);
  });

  $('#editor_temp_button').on('click', () => {
    $('#json_format').css({display: 'none'});
    $('#editor_temp').css({display: 'flex'});
  })

  $('#json_temp_button').on('click', () => {
    $('#editor_temp').css({display: 'none'});
    $('#json_format').css({display: 'flex'});
  })

  let count = 1;


  // Add questions
  $('#add-questions').click(() => {
    let questionId = `Question-${count}`;
    let label = `Question ${count}`;
    const input = `${questionId}-input`;
    const placeholder = `question: What is the question?\nchoices: ['choice1', 'choice2', 'choice3', 'choice4']\nor\nchoices: None (for textbox).`;

    $('#add-questions').before(`
    <div class="questions" id=${questionId}>
      <label> ${label} </label>
      <textarea name=${questionId} cols="50" rows="5" placeholder="${placeholder}"></textarea>
    </div>
    `);
    count++;
    console.log(questionId);
  });


  // Remove the questions
  $('#remove-questions').click(() => {
    if (count >= 2) {
      count--;
    } else {
      count = 1;
    }
  
    let questionId = `#Question-${count}`;
    console.log(questionId);
    $(questionId).remove();
  });

});

//     <input type="text" name=${questionId} class=${questionId} id=question-box placeholder="${placeholder}"><br><br>
