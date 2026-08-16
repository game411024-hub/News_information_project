from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import DateTime,func,Index
from sqlalchemy.sql.sqltypes import String,Integer,Text

#定义模型类
class Base(DeclarativeBase):
     created_at: Mapped[datetime] = mapped_column(
         DateTime,
         insert_default=func.now(),
         default=func.now(),
         comment="创建时间"
     )
     updated_at: Mapped[datetime] = mapped_column(
         DateTime,
         insert_default=func.now(),
         onupdate=func.now(),
         default=func.now(),
         comment="更新时间"
     )

class Category(Base):
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="分类ID")#表示主键
    name: Mapped[str] = mapped_column(String(50),unique= True,nullable=False, comment="分类名称")#表示不可以重复的是nullable=False
    sort_order: Mapped[int] = mapped_column(Integer,default=0,nullable=False,comment="排序")#default=0表示默认排序为0

    #创建模型类的字符串表示
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"

class News(Base):
    __tablename__ = "news"

    #创建索引，提升查询速度
    __table_args__ = (
        Index("fk_news_category_idx", "category_id"),
        Index("idx_publish_time", "publish_time")
    )
    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="新闻ID")
    title: Mapped[str] = mapped_column(String(255),nullable=False,comment="新闻标题")
    description: Mapped[str] = mapped_column(String(500),nullable=False,comment="新闻简介")#nullable的含义是该字段可以为空 = False的含义是该字段不可以为空
    content: Mapped[Text] = mapped_column(Text,nullable=False,comment="新闻内容")
    image: Mapped[str] = mapped_column(String(255),nullable=False,comment="封面图片URL")
    author: Mapped[str] = mapped_column(String(50),nullable=False,comment="作者")
    category_id: Mapped[int] = mapped_column(Integer,nullable=False,comment="分类ID")
    views: Mapped[int] = mapped_column(Integer,default=0,nullable=False,comment="浏览量")
    publish_time: Mapped[datetime] = mapped_column(DateTime,default=func.now(),insert_default=func.now(),nullable=False,comment="发布时间")

    def __repr__(self):
        return f"<News(id={self.id}, title={self.title}, description={self.description}, content={self.content}, image={self.image}, author={self.author}, category_id={self.category_id}, views={self.views}, publish_time={self.publish_time})>"

