$ErrorActionPreference='Stop'
$root='D:\작업\꿀단지\2026-09-19-아침-공복-사과-속쓰림'
$google=Join-Path $root 'post_data.json'
$naver=Join-Path $root '31_아침_공복_사과_속쓰림_네이버블로그용.html'
$backup=Join-Path $root ('backup-recipe-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $backup | Out-Null
Copy-Item -LiteralPath $google,$naver -Destination $backup
$p=Get-Content -LiteralPath $google -Raw|ConvertFrom-Json
$h=Get-Content -LiteralPath $naver -Raw
function Para([string]$text){return '<p style="font-size:1.02rem;line-height:1.9;color:#334155;margin-bottom:22px;">'+$text+'</p>'}
function ReplaceParagraphs([string]$html,[string]$needle,[string]$replacement){
  $script:count=0
  $result=[regex]::Replace($html,'<p\b[^>]*>[\s\S]*?</p>',[System.Text.RegularExpressions.MatchEvaluator]{param($m) if($m.Value.Contains($needle)){$script:count++;return $replacement};return $m.Value})
  if($script:count -ne 1){throw "Expected one paragraph: $needle, got $script:count"}
  return $result
}
$b=$p.bodyHtml
$b=ReplaceParagraphs $b '사과 껍질은 식감이 다소 질겨' (Para '껍질은 꼭 벗길 필요가 없습니다. 깨끗이 씻어 껍질째 익힌 뒤 씹기 편하면 함께 먹고, 질기게 남거나 입안에서 거슬리면 벗겨 드세요.')
$b=ReplaceParagraphs $b '껍질을 벗기면 한결 부드럽게' (Para '껍질 제거는 식감을 조절하는 선택입니다. 익히거나 껍질을 벗겼다고 속쓰림이 예방되는 것은 아니므로, 먹은 뒤 불편함이 생기면 섭취를 멈추세요.')
$b=ReplaceParagraphs $b '사과 섭취 시 위장 부담을 덜기 위해' (Para '사과는 껍질을 남길지, 얼마나 부드럽게 익힐지 취향과 씹기 편한 정도에 맞춰 준비하면 됩니다.')
$b=ReplaceParagraphs $b '사과를 얇게 썰어 전자레인지에 1~2분' (Para '따뜻한 간식으로 먹고 싶다면 사과 반쪽을 익힌 뒤 잘라 드셔 보세요. 아래는 개인 블로그의 조리 사례를 참고해 정리한 방법입니다. 속쓰림을 치료하는 식단이 아니라 식감과 향을 바꿔 즐기는 레시피입니다.')
$b=ReplaceParagraphs $b '가정에서는 700W 전자레인지를 기준으로' ((Para '사과를 흐르는 물에 씻고 반으로 자른 다음 씨와 단단한 심을 제거합니다. 반쪽을 전자레인지용 깊은 용기에 담고, 원하면 시나몬 가루를 가볍게 뿌리세요. 버터는 풍미를 더하고 싶을 때 소량 넣는 선택 재료이며 생략해도 됩니다.')+(Para '전자레인지용 뚜껑을 덮되 제품 설명에 따라 증기 배출구를 열거나 작은 틈을 남깁니다. 참고한 개인 레시피는 사과 반쪽을 4~5분 익혔고 작성자는 4분 조리했다고 합니다. 출력과 사과 크기·품종이 명시된 표준 조리 시간이 아니므로, 4~5분은 참고 범위로 삼고 중간에 익힘을 확인하세요.'))
$b=ReplaceParagraphs $b '포크로 살짝 눌렀을 때 부드럽게' ((Para '과육에 포크가 쉽게 들어가면 꺼내 잠시 식힙니다. 덜 익었다면 짧게 추가 가열하고 다시 확인하세요. 뜨거운 용기는 장갑으로 잡고, 뚜껑은 얼굴에서 먼 쪽으로 열어 증기를 피합니다. 먹기 좋은 온도가 되면 껍질째 잘라 소량부터 드세요.')+(Para '시나몬은 향을 더하는 취향 재료입니다. 버터나 향신료를 넣고 불편하다면 빼고 만들어 보세요. 익힌 뒤에도 사과가 맞지 않으면 억지로 먹을 필요는 없습니다.'))
$b=$b.Replace('사과 찌기 조리 조건과 식사 병행 시 기대와 한계','사과 반쪽을 익혀 자르는 간단 레시피와 식사 조합').Replace('껍질 손질과 기상 직후 미온수 섭취의 현실적인 도움','껍질은 취향에 맞게, 물은 수분 보충으로').Replace('껍질 벗겨 미온수 후 섭취','질긴 껍질을 선택적으로 제거').Replace('얇게 썰어 1~2분 찌기','사과 반쪽을 익힌 뒤 자르기').Replace('위장 점막의 물리적 자극을 줄이기 위한 손질과 미온수 준비','먹기 편한 식감을 위한 선택적인 껍질 손질')
$p.bodyHtml=$b
$p.faqs += [pscustomobject]@{q='익힌 사과는 껍질을 벗겨야 하나요? 시나몬도 꼭 넣어야 하나요?';a='일반 성인은 깨끗이 씻어 익힌 사과의 껍질이 씹기 편하면 함께 먹어도 됩니다. 질기거나 거슬리면 제거하세요. 시나몬과 버터는 향과 풍미를 더하는 선택 재료이며, 속쓰림 예방을 위해 넣는 재료는 아닙니다.'}
$p.references += '<span>조리 아이디어: 4월의라라, 「간단간식만드는법 | 사과 건강하게 먹는법과 사과보관방법」, 2021.10.14. 사용자가 제공한 본문 참고. 사과 반쪽·씨 제거·뚜껑 덮기·4~5분은 개인 조리 사례이며 의료 효과의 근거로 사용하지 않았습니다.</span>'
$p.references += '<a href="https://www.canada.ca/en/health-canada/services/general-food-safety-tips/microwaves.html">Health Canada — 전자레인지 조리 안전</a> — 전용 용기와 덮개, 증기가 빠져나갈 틈에 관한 안내.'
$h=ReplaceParagraphs $h '그리고 평소 소화가 잘 안 되거나' '<p>껍질은 꼭 깎지 않아도 됩니다.<br>깨끗이 씻어 익힌 뒤 씹기 편하면 함께 드세요.</p>'
$h=ReplaceParagraphs $h '질긴 껍질을 덜어내면' '<p>익혀도 껍질이 질기거나 입안에 남는 느낌이 싫다면<br>그때 벗겨 먹으면 됩니다. 내게 편한 식감으로 고르세요.</p>'
$h=ReplaceParagraphs $h '위장 부담을 덜어주는 현실적인 조절법은' '<p>따뜻한 사과 간식을 만들고 싶다면<br>반쪽째 익힌 다음 먹기 좋게 잘라보세요.</p>'
$h=ReplaceParagraphs $h '가정에서는 700W 전자레인지를 기준으로' '<p>사과를 흐르는 물에 씻어 반으로 자르고 씨와 단단한 심을 제거합니다.<br>전자레인지용 깊은 용기에 반쪽을 담고, 원하면 시나몬을 가볍게 뿌려주세요.<br>버터도 풍미를 더하고 싶을 때만 소량 넣으면 됩니다.</p>'
$h=ReplaceParagraphs $h '전용 용기에 물 1~2스푼과 함께 담아' '<p>전자레인지용 뚜껑을 덮고 증기 배출구를 열거나 작은 틈을 남겨주세요.<br>참고한 개인 레시피는 <mark>사과 반쪽을 4~5분</mark> 익히는 방법이며, 작성자는 4분 조리했다고 합니다.<br>기기 출력과 사과 크기에 따라 달라지니 중간에 익힘을 살펴주세요.</p>'
$h=ReplaceParagraphs $h '포크로 살짝 눌렀을 때 부드럽게' '<p>포크가 과육에 쉽게 들어가면 꺼내 잠시 식혀주세요.<br>덜 익었으면 짧게 추가 가열해 확인합니다.<br>장갑으로 용기를 잡고 뚜껑은 얼굴 반대쪽으로 열어 뜨거운 김을 피하세요.<br>먹기 좋은 온도가 되면 껍질째 잘라 소량부터 드시면 됩니다.</p><p>시나몬과 버터는 맛을 위한 선택 재료예요.<br>넣고 먹었을 때 불편하다면 생략하세요. 속쓰림을 막기 위해 넣는 것은 아닙니다.</p>'
$h=ReplaceParagraphs $h '내일 아침에는 따뜻한 미온수 한 잔 뒤에' '<p>따뜻한 간식이 생각나는 날에는 사과 반쪽을 익혀 잘라보세요.<br>껍질과 시나몬은 내 취향과 먹었을 때의 편안함에 맞춰 선택하면 됩니다.</p>'
$h=$h.Replace('거친 껍질을 벗기고 미온수로 달래는 요령','껍질은 취향에 맞게, 물은 편하게 한 잔').Replace('전자레인지 1~2분 조리로 사과를 찌는 방법','사과 반쪽을 4~5분 익힌 뒤 잘라 먹는 방법')
$h=$h.Replace('📚 공인 영양 데이터 및 학술 자료','📚 참고 자료')
$h=$h.Replace('<!-- 공인 참고 자료 -->','<!-- 공인 참고 자료 --><p style="font-size:0.85rem;color:#64748b;">조리 아이디어: 4월의라라의 「간단간식만드는법 | 사과 건강하게 먹는법과 사과보관방법」(2021.10.14), 사용자가 제공한 본문 참고. 4~5분은 개인 조리 사례이며 기기 출력과 사과 크기에 따라 달라집니다. 뚜껑과 증기 배출 안내는 <a href="https://www.canada.ca/en/health-canada/services/general-food-safety-tips/microwaves.html">Health Canada 조리 안전 안내</a>를 참고했습니다.</p>')
[IO.File]::WriteAllText($google,($p|ConvertTo-Json -Depth 30),[Text.UTF8Encoding]::new($false))
[IO.File]::WriteAllText($naver,$h,[Text.UTF8Encoding]::new($false))
$canonical='D:\작업\꿀단지\꿀단지 네이버\17_아침_공복_사과_속쓰림\17_아침_공복_사과_속쓰림_네이버블로그용.html'
Copy-Item -LiteralPath $canonical -Destination (Join-Path $backup 'naver-package-before.html')
Copy-Item -LiteralPath $naver -Destination $canonical
Write-Output 'Updated Google draft and both Naver copies; backups saved.'
if($p.bodyHtml -match '1~2분|1분 30초|700W|50~70g' -or $h -match '1~2분|1분 30초|700W|50~70g'){throw 'Old recipe timing remains'}
if($h -notmatch 'function copyNaverContent' -or $h -notmatch 'id="naverContent"'){throw 'Copy interface missing'}
Write-Output 'Recipe timing and Naver copy control checked.'
