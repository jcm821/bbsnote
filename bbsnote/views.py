from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# 현재 디렉토리의 models모듈에서 Board, Comment클래스를 불러옴 DB의 테이블
from .models import Board, Comment
from django.utils import timezone
from .forms import BoardForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

# 첫번째 뷰 함수 index 정의, HTTP 요청 객체인 request를 인자로 받는다.
def index(request):
    # 입력 인자 추가
    # get방식으로 요청하여 페이지를 가져오되, 페이지에 값이 없으면 1로 초기화
    page = request.GET.get('page', 1)
    # 조회
    # Board객체 목록을 생성날짜의 역순으로 정렬하여 가져옴
    board_list = Board.objects.order_by('-create_date')
    # 페이징 함수를 통해 페이지 리스트를 n개씩 볼 수 있도록 나누어 페이징을 한다
    paginator = Paginator(board_list, 5)
    # 현재 페이지를 나타내준다
    page_obj = paginator.get_page(page)

    # 변수 설정을 하지 않고 아래 render함수의 파라미터로 딕셔너리를 바로 대입해도 된다
    context = {'board_list': page_obj}
    # return HttpResponse("bbsnote에 오신것을 환영합니다!")
    # 탬플릿 파일 'bbsnote/board_list.html'을 랜더링하여 HTTP 응답 객체를 반환
    return render(request, 'bbsnote/board_list.html', context)
    # return render(request, 'bbsnote/board_list.html', {'board_list': board_list})


def detail(request, board_id):
    # Board에서 id가 board_id인 Board객체를 가져온다
    # 'Board.objects' -> SELECT * FROM bbsnote_Board
    # get(id=board_id) -> WHERE id=board_id;
    board = Board.objects.get(id=board_id)
    # 댓글을 내림차선으로 보고자 할 때
    # comment = Comment.objects.all().order_by('-create_date')
    # 이후 context에 comment추가
    
    # context변수는 템플릿에 전달되어 랜더링에 사용
    context = {'board': board}
    # 만약 comment를 foreignkey로 연결이 되어있지 않다면
    # comment = Comment.objects.get(board=board)
    # context = {'board': board, 'comment': comment}
    
    # 탬플릿 파일 'bbsnote/board_detail.html'을 랜더링하여 HTTP 응답 객체를 반환
    return render(request, 'bbsnote/board_detail.html', context)


# 기존에 로그인을 하지않고 댓글 작성을 하려 했을경우 데이터가 GET방식으로 입력되어 페이지 오류가 발생한다
# 그 이유는 아래 함수에서 POST방식일 경우에만 content=request.POST.get('content')와 같이 할당하도록 지정했었기 때문인데,
# 우리가 보낸 데이터는 GET방식이었기 때문에 content 부분에서 Not Null 제약조건 오류가 걸린것이다. 오류를 해결하기 위해서는
# 다른 함수들과 마찬가지로 조건문을 사용하여 GET방식일 경우 입력조건을 추가해주면 된다

# 로그인을 하지 않고 작성글을 올리게 되면 오류가 난다. 애너테이션 적용하여 로그인이 되었는지 우선 검사
@login_required(login_url='common:login')
def comment_create(request, board_id):
    if request.method == 'POST':
        # form = Comment(request.POST)
        # if form.is_valid():
        board = Board.objects.get(id=board_id)
        # content속성은 POST데이터 중 content 키의 값으로 설정
        # comment = Comment(board=board, content=request.POST.get('content'), create_date=timezone.now())
        # comment.save()
        # author에 요청받은 user를 출력해준다
        board.comment_set.create(content=request.POST.get('content'), create_date=timezone.now(), author=request.user)
        # 'bbsnote:detail'이라는 URL 패턴으로 리다이렉트하고 board_id라는 인자로 board.id값 전달
        # 사용자가 특정 게시판의 세부 정보 페이지로 이동할 수 있음
        # return redirect('bbsnote:detail', board_id=board.id)
    # else:
        # form = CommentForm()
    return redirect('bbsnote:detail', board_id=board_id)

@login_required(login_url='common:login')
def board_create(request):
    # 요청이 POST방식으로 들어왔으면(게시글에서 submit을 눌렀으면)
    if request.method == 'POST':
        # request.POST의 내용을 사용하여 BoardForm에 저장 후 form이라는 변수에 할당
        form = BoardForm(request.POST)
        # form에 내용이 있다면
        if form.is_valid():
            # 저장을 하되 오토커밋하지 말것(mysql의 커밋과 유사한 개념)
            board = form.save(commit=False)
            # Board model에서 auto_now_add설정을 했으므로 없어도 무방하다
            # auto설정이 되어있지 않다면 아래와 같이 선언해주면 된다
            board.create_date = timezone.now()
            # author정보에 요청되었던 현재 로그인 되어있는 user정보를 출력
            board.author = request.user
            # board를 커밋
            board.save()
            return redirect('bbsnote:index')
    # POST요청이 아니면
    else:
        form = BoardForm()
        # 'bbsnote/board_form.html' 탬플릿을 사용하여 응답을 생성하고, 템플릿 context에 'form'변수로 폼 객체를 전달
        return render(request, 'bbsnote/board_form.html', {'form': form})

# 수정과 관련된 함수 선언
# 예외처리를 추가해준다
@login_required(login_url='common:login')
def board_modify(request, board_id):
    # pk가 board_id인 객체를 가져오고, 오류가 나게 된다면 404오류를 대신 출력
    board = get_object_or_404(Board, pk=board_id)
    # 요청이 들어온 user와 board의 작성자가 틀리다면
    if request.user != board.author:
        # 요청이 들어온 user에게 오류메세지를 보낸다
        messages.error(request, '수정권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    # 수정이 들어온 경우
    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.author = request.user
            # 앞서 models.py의 update_date에 auto옵션을 사용하지 않을 때
            # board.update_data = timezone.now()
            board.save()
            return redirect('bbsnote:detail', board_id=board.id)
    # GET방식으로 넘어온 경우
    else:
        # instance매개변수에 board를 지정하면 기존의 값을 수정되는 폼에 채울 수 있다.
        form = BoardForm(instance=board)
    # 템플릿에서 사용할 수 있는 데이터를 포함하는 딕셔너리
    context = {'form': form}
    # 요청에 대해 'bbsnote/board_form.html'의 내용을 랜더링하여 context 출력
    return render(request, 'bbsnote/board_form.html', context)


# 삭제를 위한 함수를 생성해준다
@login_required(login_url='common:login')
def board_delete(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    if request.user != board.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('bbsnote:detail', board_id=board.id)
    board.delete()
    return redirect('bbsnote:index')

# 댓글 수정을 위한 함수를 생성
@login_required(login_url='common:login')
def comment_modify(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    # 요청들어온 정보의 user와 comment작성자가 다르면
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('bbsnote:detail', board_id=comment.board.id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('bbsnote:detail', board_id=comment.board.id)
    # 요청이 GET방식일 때
    else:
        form = CommentForm(instance=comment)
    context = {'comment': comment, 'form': form}
    return render(request, 'bbsnote/comment_form.html', context)

# 댓글 삭제를 위한 함수 생성
@login_required(login_url='common:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제 권한이 없습니다')
        return redirect('bbsnote:detail', board_id=comment.id)
    comment.delete()
    return redirect('bbsnote:detail', board_id=comment.board.id)