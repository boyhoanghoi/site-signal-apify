"""Shared, serializable output shapes. Contacts are observed, never verified."""

from typing import TypedDict


class Evidence(TypedDict):
    type: str
    value: str
    sourceUrl: str
    method: str


class Technology(TypedDict):
    name: str
    category: str
    evidence: str
    sourceUrl: str


class PageResult(TypedDict):
    title: str
    description: str
    companyName: str
    emails: list[str]
    phones: list[str]
    socials: dict[str, list[str]]
    contactPageUrls: list[str]
    contactFormUrls: list[str]
    technologies: list[Technology]
    evidence: list[Evidence]
    language: str
    jsonLdTypes: list[str]

