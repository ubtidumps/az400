import re
from bs4 import BeautifulSoup

with open('index.html','r') as f:
    content = f.read()

soup = BeautifulSoup(content,'html.parser')

case_study_questions = soup.find_all('div',attrs={'class':'exam-question-card'})


finalhtml = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AZ 104 Dumps</title>
        <!-- deflink == defered link (loaded later by jquery) -->
    <!-- bootstrap v4 css -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="https://www.examtopics.com/assets/css/style.css">
</head>
<body>
    
'''

for ele in case_study_questions:
    ptag  = ele.find_all('p',{'class':'card-text'})
    for pele in ptag:
        if pele.find(text = re.compile(r'To start the case study -')) is not None:
            finalhtml+=ele.prettify()
finalhtml += '''
</body>
<script src="https://code.jquery.com/jquery-2.2.4.min.js" integrity="sha256-BbhdlvQf/xTY9gja0Dq3HiwQF8LaCRTXxZKRutelT44=" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script type="text/javascript" src="https://www.examtopics.com/assets/js/comments.js"></script>
    <!-- / Comments dependencies -->
<script type="text/javascript" src="https://www.examtopics.com/assets/js/examview.js"></script>
        </script>
        <script type="text/javascript">
            /* DISCUSSIONS: */
            /* Discussion modal opened */
            $('body').on('click', ".question-discussion-button[href='#']", function (e) {
                e.preventDefault();
                let question_id = $(this).closest('.question-body').attr('data-id');
                resetDiscussionModal();
                loadDiscussionIntoModal(question_id);
                $('#discussion-modal').modal('show');
            });
            function resetDiscussionModal() {
                $('.discussion-loading-title').show();
                $('.discussion-ellipsis').show();
                $('.discussion-real-title').hide();
                $('.discussion-body').hide();
            }
            function loadDiscussionIntoModal(question_id, open_voting_comment) {
                $.ajax({
                    url: 'https://nandy-cors.herokuapp.com/https://www.examtopics.com/ajax/discussion/exam-question/' + question_id.toString(),
                    success: function (data) {
                        console.log(data)
                        $('.discussion-body').html(data);
                        $('#discussion-modal').attr("data-discussion-question-id", question_id);
                        $('.discussion-real-title').text($('.discussion-body').find('.new-comment-box').data('title'));
                        let question_object = getQuestionObjectByQuestionId(question_id);
                        if (is_question_mcq(question_object)) {
                            set_voting_configuration_by_question(question_object);
                            if (open_voting_comment) {
                                enable_voted_comment($("#discussion-modal .outer-discussion-container"));
                            }
                        }
                    },
                    error: function () {
                        $('.discussion-body').text('Server error: could not load discussion.')
                    },
                    complete: function () {
                        $('.discussion-loading-title').hide();
                        $('.discussion-ellipsis').hide();
                        $('.discussion-real-title').show();
                        $('.discussion-body').slideDown();
                    }
                });
            }
            /* END DISCUSSIONS */
    </script>
    <!-- Discussion modal -->
    <div class="modal fade" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true" id="discussion-modal">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title" id="myLargeModalLabel">
                        <span class="discussion-loading-title">
                            Loading discussion
                            <i class="ml-2 fa fa-refresh fa-spin"></i>
                        </span>
                        <span class="discussion-real-title display-none">
                            <!-- Placehodler for real discussion title -->
                        </span>
                    </h4>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="discussion-body">
                    </div>
                    <div class="discussion-ellipsis">
                        ...
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- / Discussion modal -->
    <div id="discussion-templates" class="d-none"><!-- Most Voted Answer badge --><div id="most-voted-answer-badge-template"><span class="badge badge-success most-voted-answer-badge" title="This answer is currently the most voted for in the discussion">
                Most Voted
            </span></div><!-- Voting Comment Tooltip Content --><div id="voting-comment-tooltip" class="d-none"><div class="text-left">
                A voting comment increases the vote count for the chosen answer by one. <br><br>
                Upvoting a comment with a selected answer will also increase the vote count towards that answer by one.
                So if you see a comment that you already agree with, you can upvote it instead of posting a new comment.
            </div></div><div id="edit-comment-template"><textarea class="comment-edit" style="width:100%"></textarea><br><div class="original-comment d-none"></div><a href="https://www.examtopics.com/exams/microsoft/az-204/view/#" class="btn-primary btn btn-sm comment-edit-save mr-2">Save</a><a href="https://www.examtopics.com/exams/microsoft/az-204/view/#" class="btn-warning btn btn-sm comment-edit-cancel">Cancel</a></div><div class="full-discussion-loading-spinner">
            Loading <i class="fa fa-cog fa-spin"></i> ...
        </div></div><!-- Report Comment Modal --><div class="modal fade" id="report-comment-modal" tabindex="-1" role="dialog" aria-hidden="true"><div class="modal-sm modal-dialog modal-dialog-centered"><div class="modal-content"><!-- Modal Header --><div class="modal-header"><h4 class="modal-title">Report Comment</h4><button type="button" class="close" data-dismiss="modal">×</button></div><!-- Modal body --><div class="modal-body">
                    Is the comment made by <span class="comment-report-modal-username font-italic">USERNAME</span> spam or abusive?
                </div><!-- Modal footer --><div class="modal-footer"><button type="button" class="btn btn-primary" id="modal-btn-no-2" data-dismiss="modal">Ok</button></div></div></div></div><!-- End Login Required comment modal --><input type="hidden" value="yWkfsbDzarKt422BJ3d15GzV2jZZwhhjaCVWfNExVuibpe1zyQtyqlvdvCv2BBRh" class="csrf-value"><!-- Moderate actions: --><script type="text/javascript">
        // Auto resize textarea to fit contents:
        function autoresize(textarea) {
            textarea = $(textarea)
            textarea.css('height','0px');     //Reset height, so that it not only grows but also shrinks
            textarea.css('height',(textarea[0].scrollHeight + 10) + 'px');    //Set new height
        }
        $('textarea.comment-edit').keyup(function () {
            autoresize(this);
        });
    </script>
</html>
'''


with open('casestudies/index.html','w') as f1:
    f1.write(finalhtml)