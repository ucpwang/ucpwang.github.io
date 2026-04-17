---
title: 'Astro Content Collections 완벽 가이드'
date: 2025-12-30
description: 'Astro의 Content Collections로 타입 안전한 마크다운 블로그를 만드는 방법. 스키마 정의부터 쿼리, 렌더링까지 실전 중심으로 설명합니다.'
tags: ['Astro', 'TypeScript', '블로그', '개발']
draft: false
---

## Content Collections란

Astro 2.0에 도입된 Content Collections는 마크다운 파일을 **타입 안전하게** 관리하는 시스템이다.

기존 방식의 문제:

```js
// 예전 방식 — frontmatter가 뭔지 모름
const posts = await Astro.glob('./posts/*.md');
posts[0].frontmatter.title; // string | undefined, 타입 불안
posts[0].frontmatter.date; // 실제로 Date인지 string인지 불명확
```

Content Collections로:

```ts
// 스키마로 보장된 타입
const posts = await getCollection('blog');
posts[0].data.title; // string (보장됨)
posts[0].data.date; // Date (보장됨)
```

## 스키마 정의

`src/content/config.ts`에서 Zod로 스키마를 정의한다.

```ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(), // string을 Date로 자동 변환
    description: z.string(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
    cover: z.string().optional(), // 없어도 됨
  }),
});

export const collections = { blog };
```

`z.coerce.date()`를 쓰면 `2026-01-01` 형태의 문자열을 자동으로 `Date` 객체로 변환한다.

## 파일 네이밍 컨벤션

```
src/content/blog/
├── 2026-04-15-astro-design-system.md
├── 2026-03-28-neumorphism-dark.md
└── 2025-12-30-content-collections.md
```

날짜를 파일명 앞에 붙이면 폴더 정렬 시 자동으로 시간순이 된다.

## 포스트 쿼리하기

```ts
import { getCollection } from 'astro:content';

// 전체 포스트 (draft 제외)
const posts = await getCollection('blog', ({ data }) => !data.draft);

// 최신순 정렬
const sorted = posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

// 특정 태그 필터
const tagged = posts.filter((p) => p.data.tags.includes('Astro'));
```

## 동적 라우팅

```astro
---
// src/pages/blog/[...slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
```

`post.render()`가 마크다운을 렌더링한 `Content` 컴포넌트를 반환한다.

## 이미지 처리

Astro 3.0부터 Content Collections에서 이미지 최적화가 기본 지원된다.

```ts
schema: z.object({
  cover: image().optional(), // 자동 최적화
});
```

```astro
import {Image} from 'astro:assets';

<Image src={post.data.cover} alt="커버 이미지" />
```

## 마무리

Content Collections는 처음엔 설정이 번거롭게 느껴지지만, 타입 안전성과 자동완성이 주는 개발 경험이 압도적이다. 마크다운 파일 하나 수정하면 타입 에러가 즉시 잡힌다.

블로그 규모가 커질수록 이 차이는 더 극명하게 드러난다.
