<script>
  import fastapi from "../lib/api"
  import { link } from 'svelte-spa-router'
  import { page, keyword, is_login, nickname } from "../lib/store"
  import moment from 'moment/min/moment-with-locales'
  moment.locale('ko') // 한국식 날짜 형식

  let plan_list = []
  let size = 10
  let total = 0
  let kw = ''
  $: total_page = Math.ceil(total/size)

  function get_plan_list() {
    let params = {
      page: $page,
      size: size,
      keyword: $keyword,
    }
    fastapi('get', '/api/plan/list', params, (json) => {
      plan_list = json.plan_list
      total = json.total
      kw = $keyword
    })
  }

  // 반응형 구문 ($page가 변하면 함수 다시 호출)
  $: $page, $keyword, get_plan_list()
</script>

<div class="container my-3">

  <div class="d-flex justify-content-between align-items-center mb-2">
    <h1>교육활동계획안</h1>
    {#if $is_login && $nickname === "admin"}
      <a use:link href="/plan-create" class="btn btn-outline-primary">새 계획안 등록</a>
    {/if}
  </div>

  <div class="row my-2">
    <div class="col-6">
      <div class="input-group">
          <input type="text" class="form-control" bind:value="{kw}">
          <button class="btn btn-outline-secondary" on:click={() => {$keyword = kw, $page = 0}}>
              찾기
          </button>
      </div>
  </div>
  </div>
  
  <table class="table table-striped">
      <thead>
      <tr class="table-dark">
          <th>번호</th>
          <th>제목</th>
          <th>주제</th>
          <th>작성일시</th>
      </tr>
      </thead>
      <tbody>
        {#each plan_list as plan, i}
        <tr>
            <td>{ total - ($page * size) - i }</td>
            <td>
              <a use:link href="/detail/{plan.id}">{plan.title}</a>
            </td>
            <td>{@html plan.topic}</td>
            <td>{moment(plan.create_date).format("YYYY년 MM월 DD일")}</td>
        </tr>
        {/each}
        </tbody>
    </table>

    <!-- 페이징처리 시작 -->
    <ul class="pagination justify-content-center">
      <!-- 처음페이지 -->
      <li class="page-item {$page <= 0 && 'disabled'}">
        <button class="page-link" on:click="{() => $page = 0}">처음</button>
    </li>
      <!-- 이전페이지 -->
      <li class="page-item {$page <= 0 && 'disabled'}">
          <button class="page-link" on:click="{() => $page--}">이전</button>
      </li>
      <!-- ... -->
      {#if $page >= 4}
      <li class="page-item">
        <button class="page-link" on:click="{() => $page -= 4}">...</button>
      </li>
      {/if}
      <!-- 페이지번호 -->
      {#each Array(total_page) as _, loop_page}
      {#if loop_page >= $page-3 && loop_page <= $page+3} 
      <li class="page-item {loop_page === $page && 'active'}">
          <button on:click="{() => $page = loop_page}" class="page-link">{loop_page+1}</button>
      </li>
      {/if}
      {/each}
      <!-- ... -->
      {#if $page < total_page-4}
      <li class="page-item">
        <button class="page-link" on:click="{() => $page+=4}">...</button>
      </li>
      {/if}
      <!-- 다음페이지 -->
      <li class="page-item {$page >= total_page-1 && 'disabled'}">
          <button class="page-link" on:click="{() => $page++}">다음</button>
      </li>
      <!-- 마지막페이지 -->
      <li class="page-item {$page >= total_page-1 && 'disabled'}">
        <button class="page-link" on:click="{() => $page = total_page-1}">마지막</button>
      </li>
  </ul>
  <!-- 페이징처리 끝 -->

</div>