from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    description: str
    url: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    importance: int = 3  # 1-5

    def display(self) -> str:
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return (
            f"关键词: {self.keyword}\n"
            f"描述: {self.description}\n"
            f"URL: {self.url}\n"
            f"标签: {tag_str}\n"
            f"创建时间: {self.created_at}\n"
            f"重要度: {'★' * self.importance}{'☆' * (5 - self.importance)}\n"
        )


@dataclass
class KeywordCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> Optional[KeywordNote]:
        for note in self.notes:
            if keyword in note.keyword:
                return note
        return None

    def find_by_tag(self, tag: str) -> List[KeywordNote]:
        return [note for note in self.notes if tag in note.tags]

    def list_all(self, sort_by: str = "created_at") -> None:
        if sort_by == "importance":
            sorted_notes = sorted(self.notes, key=lambda x: x.importance, reverse=True)
        else:
            sorted_notes = sorted(self.notes, key=lambda x: x.created_at, reverse=True)

        for idx, note in enumerate(sorted_notes, 1):
            print(f"--- 笔记 {idx} ---")
            print(note.display())

    def summary(self) -> str:
        total = len(self.notes)
        avg_imp = sum(n.importance for n in self.notes) / total if total else 0
        all_tags = set()
        for n in self.notes:
            all_tags.update(n.tags)
        return f"总笔记数: {total}, 平均重要度: {avg_imp:.1f}, 标签数: {len(all_tags)}"


def format_all_notes(collection: KeywordCollection, heading: str = "关键词笔记汇总") -> str:
    lines = [heading, "=" * len(heading), ""]
    for idx, note in enumerate(collection.notes, 1):
        lines.append(f"[{idx}] {note.keyword}")
        lines.append(f"    描述: {note.description}")
        lines.append(f"    URL: {note.url}")
        if note.tags:
            lines.append(f"    标签: {', '.join(note.tags)}")
        lines.append(f"    重要度: {note.importance}/5")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    sample_url = "https://indexportal-leyu.com.cn"
    sample_keyword = "乐鱼体育"

    note1 = KeywordNote(
        keyword=sample_keyword,
        description="乐鱼体育平台关键词笔记示例",
        url=sample_url,
        tags=["体育", "娱乐", "平台"],
        importance=4
    )

    note2 = KeywordNote(
        keyword="数据分析",
        description="用于体育平台用户行为分析",
        url=sample_url + "/analytics",
        tags=["技术", "数据"],
        importance=3
    )

    note3 = KeywordNote(
        keyword="版本更新",
        description="乐鱼体育移动端新功能发布记录",
        url=sample_url + "/changelog",
        tags=["开发", "发布"],
        importance=5
    )

    collection = KeywordCollection()
    collection.add_note(note1)
    collection.add_note(note2)
    collection.add_note(note3)

    print("=== 按时间排序 ===")
    collection.list_all(sort_by="created_at")

    print("\n=== 按重要度排序 ===")
    collection.list_all(sort_by="importance")

    print("\n=== 汇总 ===")
    print(collection.summary())

    print("\n=== 格式化输出 ===")
    output = format_all_notes(collection)
    print(output)

    print("\n=== 按标签查找 ===")
    tech_notes = collection.find_by_tag("技术")
    for n in tech_notes:
        print(f"找到: {n.keyword}")


if __name__ == "__main__":
    main()