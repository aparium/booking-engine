import argparse
import cssutils

def merge_duplicate_css(css: str) -> str:
    """
    Detects duplicate CSS selectors or identical property sets and merges them.
    """
    stylesheet = cssutils.parseString(css)
    rules_map = {}

    # Iterate over rules in the stylesheet
    for rule in stylesheet.cssRules:
        if rule.type == cssutils.css.CSSRule.STYLE_RULE:
            properties = tuple(sorted((p.name, p.value) for p in rule.style))
            if properties in rules_map:
                # Merge selectors if identical properties exist
                rules_map[properties].extend(rule.selectorText.split(","))
            else:
                rules_map[properties] = rule.selectorText.split(",")

    # Generate the merged CSS
    merged_css = []
    for properties, selectors in rules_map.items():
        selector_text = ",".join(sorted(set(selectors)))  # Merge duplicate selectors
        props_text = ";\n".join([f"{name}: {value}" for name, value in properties]) + ";"
        merged_css.append(f"{selector_text} {{\n{props_text}\n}}")

    return "\n\n".join(merged_css)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Merge duplicate CSS selectors or rules.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input CSS file.")
    parser.add_argument("-o", "--output", required=True, help="Path to save the optimized CSS file.")
    args = parser.parse_args()

    # Read CSS content from the input file
    with open(args.input, "r") as file:
        css_input = file.read()

    # Merge and optimize the CSS
    optimized_css = merge_duplicate_css(css_input)

    # Save the result to the specified output file
    with open(args.output, "w") as file:
        file.write(optimized_css)

    print(f"Optimized CSS saved to {args.output}")