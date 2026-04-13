import streamlit as st
import math

st.set_page_config(page_title="Windows Calculator", layout="centered")


defaults = {
    "expr": "0",
    "prev": None,
    "operator": None,
    "waiting": False,
    "just_calc": False,
    "expr_display": "",
    "memory": None,
    "history": [],
    "error": False,
    "angle_mode": "DEG",
    "fe_mode": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def _round(n):
    return float(f"{n:.14g}")

def _fmt(n):
    if n is None:
        return "0"

    if st.session_state.fe_mode:
        return f"{n:.6e}"   
    else:
        return f"{n:.14g}"  

def _set_error(msg="Error"):
    st.session_state.expr = msg
    st.session_state.error = True
    st.session_state.prev = None
    st.session_state.operator = None

def _compute(a, b, op):
    if op == "+": return _round(a + b)
    if op == "-": return _round(a - b)
    if op == "*": return _round(a * b)
    if op == "/":
        if b == 0:
            _set_error("Cannot divide by zero")
            return None
        return _round(a / b)
    
    if op == "^": return _round(a ** b)

    if op == "%": return _round(a % b)


def press(val):
    if st.session_state.error:
        st.session_state.expr = "0"
        st.session_state.error = False

    if val in ("×", "÷", "＋", "−"):
        op_map = {
            "×": "*",
            "÷": "/",
            "＋": "+",
            "−": "-"
        }
        set_op(op_map[val])
        return

    if val == "%":
        calcFunc("percent")
        return

    if val == "." and "." in st.session_state.expr:
        return

    if st.session_state.waiting:
        st.session_state.expr = val
        st.session_state.waiting = False
    else:
        if st.session_state.expr == "0":
            st.session_state.expr = val
        else:
            st.session_state.expr += val

def set_op(op):
    cur = float(st.session_state.expr)

    if st.session_state.operator:
        res = _compute(st.session_state.prev, cur, st.session_state.operator)
        if res is None: return
        st.session_state.prev = res
        st.session_state.expr = _fmt(res)
    else:
        st.session_state.prev = cur

    st.session_state.operator = op
    st.session_state.waiting = True

def calculate():
    if st.session_state.operator is None:
        return

    a = st.session_state.prev
    b = float(st.session_state.expr)

    res = _compute(a, b, st.session_state.operator)
    if res is None: return

    st.session_state.history.insert(0, {
        "expr": f"{a} {st.session_state.operator} {b}",
        "result": res
    })

    st.session_state.expr = _fmt(res)
    st.session_state.prev = None
    st.session_state.operator = None

    if st.session_state.error:
        return

def clear():
    for k, v in defaults.items():
        st.session_state[k] = v

def backspace():
    st.session_state.expr = st.session_state.expr[:-1] or "0"

def toggle_sign():
    if st.session_state.expr.startswith("-"):
        st.session_state.expr = st.session_state.expr[1:]
    else:
        st.session_state.expr = "-" + st.session_state.expr

def calcFunc(fn):
    n = float(st.session_state.expr)

    if fn == "sqrt":
        if n < 0:
            _set_error("Invalid input")
            return
        st.session_state.expr = _fmt(math.sqrt(n))

    elif fn == "sq":
        st.session_state.expr = _fmt(n * n)

    elif fn == "recip":
        if n == 0:
            _set_error("Cannot divide by zero")
            return
        st.session_state.expr = _fmt(1 / n)

    elif fn == "percent":
        if st.session_state.prev is not None:
            st.session_state.expr = _fmt(st.session_state.prev * n / 100)
        else:
            st.session_state.expr = _fmt(n / 100)

    elif fn == "ce":
        st.session_state.expr = "0"

    elif fn == "pi":
        st.session_state.expr = str(math.pi)

    elif fn == "e":
        st.session_state.expr = str(math.e)

    elif fn == "log":
        if n <= 0:
            _set_error("Invalid input")
            return
        st.session_state.expr = _fmt(math.log10(n))

    elif fn == "ln":
        if n <= 0:
            _set_error("Invalid input")
            return
        st.session_state.expr = _fmt(math.log(n))

    elif fn == "abs":
        st.session_state.expr = _fmt(abs(n))

    elif fn == "fact":
        if n < 0 or int(n) != n:
            _set_error("Invalid input")
            return
        st.session_state.expr = _fmt(math.factorial(int(n)))

    elif fn == "exp":
        st.session_state.expr = _fmt(math.exp(n))

    elif fn == "pow":
        st.session_state.prev = float(st.session_state.expr)
        st.session_state.operator = "^"
        st.session_state.waiting = True

    elif fn == "ten_pow":
        st.session_state.expr = _fmt(10 ** n)

    elif fn == "mod":
        st.session_state.prev = float(st.session_state.expr)
        st.session_state.operator = "%"
        st.session_state.waiting = True


def memOp(op):
    n = float(st.session_state.expr)

    if op == "MS":
        st.session_state.memory = _round(n)

    elif op == "MR":
        if st.session_state.memory is not None:
            st.session_state.expr = _fmt(st.session_state.memory)
            st.session_state.waiting = False
            st.session_state.just_calc = False

    elif op == "M+":
        m = st.session_state.memory or 0
        st.session_state.memory = _round(m + n)

    elif op == "M-":
        m = st.session_state.memory or 0
        st.session_state.memory = _round(m - n)

    elif op == "MC":
        st.session_state.memory = None

def toggle_deg():
    if st.session_state.angle_mode == "DEG":
        st.session_state.angle_mode = "RAD"
    else:
        st.session_state.angle_mode = "DEG"

def toggle_fe():
    st.session_state.fe_mode = not st.session_state.fe_mode


st.markdown("""
<style>
.display {
    width: 500px;
    background-color: #D3D3D3;
    color: black;
    font-size: 40px;
    text-align: right;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
        f"<div class='display'>{st.session_state.expr}</div>",
        unsafe_allow_html=True
    )
left_col, right_col = st.columns([3, 1.15])

with left_col:

    tab_std, tab_sci = st.tabs(["  Standard  ", "  Scientific  "])
    
    if st.session_state.memory is not None:
        st.markdown(
            f"<div class='mem-badge'>M = {_fmt(st.session_state.memory)}</div>",
            unsafe_allow_html=True
        )
    
    
    with tab_std:
        cols = st.columns(5)

        has_mem = st.session_state.memory is not None

        for i, op in enumerate(["MC","MR","M+","M-","MS"]):
    
            disabled = (op in ("MC", "MR")) and not has_mem

            cols[i].button(
                op,
                on_click=memOp,   
                args=(op,),
                disabled=disabled
            )

    
        cols = st.columns(4)
        cols[0].button("¹/x", on_click=calcFunc, args=("recip",), key="recip_std")
        cols[1].button("x²", on_click=calcFunc, args=("sq",), key="sq_std")
        cols[2].button("√x", on_click=calcFunc, args=("sqrt",), key="sqrt_std")
        cols[3].button("CE", on_click=calcFunc, args=("ce",), key="ce_std")

        
        cols = st.columns(4)
        cols[0].button("C", on_click=clear, key="clear_std")
        cols[1].button("⌫", on_click=backspace, key="backspace_std")
        cols[2].button("%", on_click=press, args=("%",), key="%")
        cols[3].button("÷", on_click=press, args=("÷",), key="div")

        
        nums = [
            ("7","8","9","×"),
            ("4","5","6","−"),
            ("1","2","3"," ＋ "),
            ("+/-","0",".","=")
        ]

        for r, row in enumerate(nums):
            cols = st.columns(4)
            for i, val in enumerate(row):
                if val == "=":
                    cols[i].button(val, on_click=calculate, key=f"std_eq_{r}_{i}")
                elif val == "+/-":
                    cols[i].button(val, on_click=toggle_sign, key=f"std_sign_{r}_{i}")
                else:
                    cols[i].button(val, on_click=press, args=(val,), key=f"std_{r}_{i}_{val}")


    with tab_sci:

        cols = st.columns(5)
        cols[0].button(
            st.session_state.angle_mode,
            on_click=toggle_deg,
            key="deg_toggle"
        )

        cols[1].button(
            "F-E",
            on_click=toggle_fe,
            key="fe_toggle"
        )

        cols = st.columns(5)
        cols[0].button("2ⁿ")
        cols[1].button("π", on_click=calcFunc, args=("pi",), key="pi")
        cols[2].button("e", on_click=calcFunc, args=("e",), key="e")
        cols[3].button("C", on_click=clear, key="c")
        cols[4].button("⌫", on_click=backspace, key="back_space")

        cols = st.columns(5)
        cols[0].button("x²", on_click=calcFunc, args=("sq",), key="sq_sci")
        cols[1].button("¹/x", on_click=calcFunc, args=("recip",), key="recip_sci")
        cols[2].button("|x|", on_click=calcFunc, args=("abs",), key="mod")
        cols[3].button("exp", on_click=calcFunc, args=("exp",), key="exp")
        cols[4].button("mod", on_click=calcFunc, args=("mod",), key="mod_btn")

        cols = st.columns(5)
        cols[0].button("√x", on_click=calcFunc, args=("sqrt",), key="sq_root")
        cols[1].button("(", on_click=press, args=("(",), key="(")
        cols[2].button(")", on_click=press, args=(")",), key=")")
        cols[3].button("n!", on_click=calcFunc, args=("fact",), key="!")
        cols[4].button("÷", on_click=press, args=("÷",), key="/")

        rows = [
            ("xʸ","7","8","9","×"),
            ("10ˣ","4","5","6","−"),
            ("log","1","2","3","＋"),
            ("ln","+/-","0",".","=")
        ]

        for r, row in enumerate(rows):
            cols = st.columns(5)
            for i, val in enumerate(row):

                if val == "=":
                    cols[i].button(val, on_click=calculate, key=f"sci_eq_{r}_{i}")

                elif val == "+/-":
                    cols[i].button(val, on_click=toggle_sign,key=f"sci_sign_{r}_{i}")

                elif val == "log":
                    cols[i].button(val, on_click=calcFunc, args=("log",), key=f"sci_log_{r}_{i}")

                elif val == "ln":
                    cols[i].button(val, on_click=calcFunc, args=("ln",), key="ln")

                elif val == "xʸ":
                    cols[i].button(val, on_click=calcFunc, args=("pow",), key=f"sci_pow_{r}_{i}")

                elif val == "10ˣ":
                    cols[i].button(val, on_click=calcFunc, args=("ten_pow",), key=f"sci_10pow_{r}_{i}")

                else:
                    cols[i].button(val, on_click=press, args=(val,), key=f"sci_{r}_{i}_{val}")

                

with right_col:
    

    for h in st.session_state.history:
        st.write(f"{h['expr']} = {h['result']}")



st.markdown("""
<style>

.display {
    width: 500px;
    background-color: #D3D3D3;
    color: black;
    font-size: 40px;
    text-align: right;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 10px;
}

div.stButton > button {
    width: 100px;
    height: 55px;
    font-size: 18px;
    border-radius: 8px;
    font-weight: bold;
    color: black !important;
    background-color: #D3D3D3 !important;
}

div.stButton {
    margin: 3px;
}

div.stButton > button:hover {
    background-color: #C0C0C0 !important;
}

</style>
""", unsafe_allow_html=True)