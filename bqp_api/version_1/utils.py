import re

MAX_GATES, MAX_DEPTH = 10_000, 1_000
_SKIP = ("OPENQASM", "include", "qreg", "creg", "qubit", "bit", "barrier", "//")


def check_circuit(qasm: str) -> str | None:
    """Return an error message if the circuit is too large, else None."""
    gates, depth, layer = 0, 0, {}
    qasm = re.sub(r"gate\s[^{]*\{[^}]*\}", "", qasm)  # drop gate definitions
    for stmt in qasm.split(";"):
        stmt = stmt.strip()
        if not stmt or stmt.startswith(_SKIP):
            continue
        qubits = re.findall(r"\w+\[\d+\]", stmt.split("->")[0].split("=")[-1])
        gates += 1
        level = max((layer.get(q, 0) for q in qubits), default=0) + 1
        layer.update(dict.fromkeys(qubits, level))
        depth = max(depth, level)
        if gates > MAX_GATES:
            return f"gate count > {MAX_GATES}"
        if depth > MAX_DEPTH:
            return f"depth > {MAX_DEPTH}"
    return None