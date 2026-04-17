export function tagToSlug(tag: string): string {
  return tag
    .toLowerCase()
    .replace(/[/\s]+/g, '-')
    .replace(/[^a-z0-9가-힣-]/g, '')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

export function slugToTag(slug: string, allTags: string[]): string | undefined {
  return allTags.find((t) => tagToSlug(t) === slug);
}
