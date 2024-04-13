from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ._mplist import MathProblemList
from ._problem import MathProblem

FLD = "datasets"

class Datasets:

    @staticmethod
    def read_dataset(flname: Union[Path, str]) -> MathProblemList:
        rtn = MathProblemList()
        p = Path(__file__).parent.absolute()
        rtn.import_toml(p.joinpath(FLD, flname))
        return rtn

    @classmethod
    def Ahren_Jackson(cls) -> MathProblemList:
        return cls.read_dataset("Ahren_Jackson.toml")

    @staticmethod
    def problem_space(operation: str,
                      operant1: List[int],
                      operant2: List[int],
                      incorrect_deviations: Optional[List[int]] = None,
                      decade_results=True,
                      tie_problem=True,
                      negative_results=True,
                      properties: Optional[Dict[str, Any]] = None) -> MathProblemList:
        """creates a MathProblemList comprising the defined problem space
        """
        if incorrect_deviations is None:
            inc_dev = set()
        else:
            inc_dev = set(incorrect_deviations)
        inc_dev.add(0)  # correct result

        rtn = MathProblemList()
        for op1 in operant1:
            for op2 in operant2:
                if tie_problem or op1 != op2:
                    for dev in inc_dev:
                        p = MathProblem(op1, operation, op2)
                        correct = p.calc()
                        assert isinstance(correct, int)
                        result = correct + dev
                        if not decade_results and (result % 10 == 0 or correct % 10 == 0):
                            continue
                        if not negative_results and (result < 0 or correct < 0):
                            continue

                        p.result = p.calc() + dev
                        if isinstance(properties, Dict):
                            p.update_properties(properties)
                        rtn.append(p)
        return rtn