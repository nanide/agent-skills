#!/usr/bin/env node
import fs from "node:fs";
import process from "node:process";

const file = process.argv[2];
if (!file) {
	console.error("Usage: node check-plan.mjs <plan.md>");
	process.exit(2);
}

let source;
try {
	source = fs.readFileSync(file, "utf8");
} catch (error) {
	console.error(`${file}: ${error.message}`);
	process.exit(1);
}

const problems = [];
function fail(line, message) {
	problems.push(`${file}:${line}: ${message}`);
}

// Fenced examples can contain complete plans, including valid headings and fields.
function proseLines(source) {
	const raw = source.split(/\r?\n/);
	const start = raw[0] === "---" ? raw.indexOf("---", 1) + 1 : 0;
	const lines = [];
	let fence;
	for (let i = start; i < raw.length; i++) {
		const text = raw[i];
		const match = text.match(/^ {0,3}(`{3,}|~{3,})(.*)$/);
		if (fence) {
			if (match && match[1][0] === fence[0] && match[1].length >= fence.length && !match[2].trim()) {
				fence = undefined;
			}
		} else if (match && (match[1][0] === "~" || !match[2].includes("`"))) {
			fence = match[1];
		} else {
			lines.push({ text, n: i + 1 });
		}
	}
	return lines;
}

const lines = proseLines(source);
if (!lines.some(({ text }) => /^# \S/.test(text))) fail(1, "missing plan title");
const sections = [];
for (const line of lines) {
	const heading = line.text.match(/^##\s+(.+?)\s*$/);
	if (heading) sections.push({ ...line, title: heading[1], body: [] });
	else sections.at(-1)?.body.push(line);
}

const program = sections.findIndex(({ title }) => title === "Program checklist");
const close = sections.findIndex(({ title }) => title === "Close the program");
const legacy = program !== -1;
let units;
if (legacy) {
	if (close <= program) fail(sections[program].n, 'expected "## Close the program" after the program checklist');
	units = sections.slice(program + 1, close < 0 ? undefined : close);
	for (const section of sections.slice(close < 0 ? sections.length : close + 1)) {
		if (!section.title.startsWith("Appendix")) {
			fail(section.n, `"## ${section.title}" after Close the program is not an appendix`);
		}
	}
	// Retain prose checks for the original template. The opening checkpoint can contain a verbatim user request.
	for (const { text, n } of lines.filter(({ n }) => n >= sections[0].n)) {
		const prose = text
			.replace(/(?<!`)(`+)(?!`)(.*?)(?<!`)\1(?!`)/g, "`")
			.replace(/!\[[^\]]*\]\([^)]*\)/g, "")
			.replace(/\]\([^)]*\)/g, "]");
		if (/[\u2013\u2014]/.test(prose)) fail(n, "long dash");
		if (/[\u2018\u2019\u201c\u201d]/.test(prose)) fail(n, "curly quote");
		if (/: \S/.test(prose)) fail(n, "mid-sentence colon");
	}
} else {
	units = sections.filter(({ title }) => !/^Appendix(?:\s|\.|$)/i.test(title));
}
if (!units.length) fail(1, "no change sections found");

const fieldNames = ["Depends on", "Files", "Build", "Result", "Unit", "Live", "Performance", "Review"];
const aliases = new Map([
	["You see", "Result"], ["Verify, unit", "Unit"], ["Verify, live", "Live"],
	["Verify, perf", "Performance"], ["Review gate", "Review"],
]);
const checkbox = /^\s*-\s+\[[ xX]\]\s*/;
const listMarker = /^\s*[-*]\s+/;
const emptyAnswer = /^(?:n\/a|none|todo|tbd|\.\.\.|<[^>]+>)[.!]?$/i;
const exemption = /^(?:n\/a|none|not applicable)(?:[.:]\s*(.*)|$)/i;

function hasDetail(text) {
	return Boolean(text.trim()) && !emptyAnswer.test(text.trim());
}

function fieldsOf(unit) {
	const fields = new Map();
	let field;
	let checkboxEvidence = false;
	for (const line of unit.body) {
		const text = line.text.replace(checkbox, "").trim();
		const label = (legacy ? line.text : text).match(/^\*\*([^*]+?)\.?\*\*\s*(.*)$/);
		const name = label && (aliases.get(label[1]) ?? label[1]);
		if (label && (fieldNames.includes(name) || name === "Merge")) {
			if (fields.has(name)) fail(line.n, `${unit.title}: duplicate ${name} field`);
			// The old verification headers contain instructions for writing the plan, not its evidence.
			checkboxEvidence = legacy && label[1].startsWith("Verify,");
			field = { n: line.n, content: checkboxEvidence ? [] : [label[2]] };
			fields.set(name, field);
		} else if (!legacy && (label || /^#{1,6}\s/.test(text))) {
			field = undefined;
		} else if (field && text && (!checkboxEvidence || checkbox.test(line.text))) {
			field.content.push(text.replace(listMarker, "").trim());
		}
	}
	return fields;
}

function part(field, label) {
	const prefix = label + ".";
	return field.content.find((line) => line.startsWith(prefix))?.slice(prefix.length).trim() ?? "";
}

const previousIds = new Set();
for (const unit of units) {
	const fields = fieldsOf(unit);
	const value = (name) => fields.get(name)?.content.join(" ").trim() ?? "";
	const issue = (name, message) => fail(fields.get(name)?.n ?? unit.n, `${unit.title}: ${message}`);
	for (const name of fieldNames) {
		const text = value(name);
		if (!text) {
			issue(name, `supply ${name} with its ${name === "Depends on" ? "dependencies or None" : "plan details"}`);
		} else if (!["Depends on", "Performance", "Review"].includes(name) && (!hasDetail(text) || exemption.test(text))) {
			issue(name, `supply ${name} with its plan details`);
		}
	}

	if (legacy) {
		const perf = fields.get("Performance");
		if (perf) {
			for (const label of ["Metric", "Probe", "Baseline", "Rule"]) {
				if (!hasDetail(part(perf, label))) issue("Performance", `supply the performance ${label.toLowerCase()}`);
			}
		}
		const review = value("Review");
		if (review && !review.startsWith("None.") && !["operator", "screenshot", "video"].every((word) => review.includes(word))) {
			issue("Review", "describe the operator review and its screenshot and video evidence, or use the legacy None. exemption");
		}
		continue;
	}
	const id = unit.title.match(/^([\w-]+)\.\s+\S/)?.[1];
	if (!id) fail(unit.n, `${unit.title}: use a heading like "## LIST. Show installed skills"`);
	if (previousIds.has(id)) fail(unit.n, `${unit.title}: duplicate change ID ${id}`);
	const dependencies = value("Depends on").replace(/\.$/, "");
	if (dependencies && !/^none$/i.test(dependencies)) {
		for (const parent of dependencies.split(/\s*,\s*/)) {
			if (!previousIds.has(parent)) issue("Depends on", `dependency "${parent}" must name an earlier change`);
		}
	}
	if (id) previousIds.add(id);

	for (const name of ["Performance", "Review"]) {
		const field = fields.get(name);
		if (!field || !value(name)) continue;
		const exempt = value(name).match(exemption);
		if (exempt) {
			if (!hasDetail(exempt[1] ?? "")) issue(name, `explain why ${name} does not apply`);
			continue;
		}
		if (name === "Review") {
			if (!hasDetail(part(field, "Evidence"))) issue(name, "name the operator's interaction review evidence under Evidence.");
			if (!field.content.some((line) => !line.startsWith("Evidence.") && hasDetail(line))) {
				issue(name, "describe the interaction the operator reviews");
			}
		} else {
			for (const detail of ["Metric", "Probe", "Baseline", "Limit"]) {
				if (!hasDetail(part(field, detail))) issue(name, `supply the performance ${detail.toLowerCase()}`);
			}
			if (hasDetail(part(field, "Limit")) && !/\d/.test(part(field, "Limit"))) {
				issue(name, "give the numerical failure threshold under Limit.");
			}
		}
	}
}

for (const problem of problems) console.error(problem);
console.log(`${units.length} PR sections, ${problems.length} problems`);
process.exit(problems.length ? 1 : 0);
