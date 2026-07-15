"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { marketplaceName, plugins } from "../catalog.generated";
import { CopyCommand } from "./CopyCommand";

const categories = [
  "All",
  ...Array.from(new Set(plugins.map((plugin) => plugin.category))),
];

export function Catalog() {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("All");

  const matches = useMemo(() => {
    const needle = query.trim().toLowerCase();
    return plugins.filter((plugin) => {
      const matchesCategory =
        category === "All" || plugin.category === category;
      const haystack = [
        plugin.name,
        plugin.slug,
        plugin.description,
        plugin.longDescription,
        ...plugin.skills.map((skill) => skill.name + " " + skill.description),
      ]
        .join(" ")
        .toLowerCase();
      return matchesCategory && (!needle || haystack.includes(needle));
    });
  }, [category, query]);

  return (
    <div>
      <div className="catalog-tools">
        <label className="search-field">
          <span className="sr-only">Search plugins</span>
          <input
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search plugins or skills"
            type="search"
            value={query}
          />
        </label>
        <div className="filter-list" aria-label="Filter by category">
          {categories.map((item) => (
            <button
              aria-pressed={category === item}
              key={item}
              onClick={() => setCategory(item)}
              type="button"
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      <div className="catalog-grid">
        {matches.map((plugin, index) => (
          <article
            className={"plugin-card card-variant-" + (index % 4)}
            key={plugin.slug}
          >
            <div className="card-topline">
              <span>{plugin.category}</span>
              <span>{plugin.counts.skills} skills</span>
            </div>
            <div>
              <h3>{plugin.name}</h3>
              <p>{plugin.shortDescription}</p>
            </div>
            <ul className="skill-preview" aria-label="Featured skills">
              {plugin.skills.slice(0, 4).map((skill) => (
                <li key={skill.name}>{skill.name}</li>
              ))}
            </ul>
            <div className="card-actions">
              <CopyCommand
                command={
                  "codex plugin add " + plugin.slug + "@" + marketplaceName
                }
                compact
              />
              <Link href={"/plugins/" + plugin.slug}>Details</Link>
            </div>
          </article>
        ))}
      </div>

      {matches.length === 0 && (
        <div className="empty-state">
          <p>No plugin matches that search.</p>
          <button
            onClick={() => {
              setQuery("");
              setCategory("All");
            }}
            type="button"
          >
            Reset catalog
          </button>
        </div>
      )}
    </div>
  );
}
