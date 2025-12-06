#!/bin/bash

# Define text colors for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}>>> Starting Code Quality Check...${NC}"

# 1. Run isort (Import Sorter)
echo -e "\n${GREEN}[1/4] Running isort (Import Sorter)...${NC}"
# --atomic prevents isort from saving broken code if it crashes
isort backend/ --atomic
if [ $? -ne 0 ]; then
    echo -e "${RED} isort failed.${NC}"
    exit 1
fi

# 2. Run YAPF (Formatter)
echo -e "\n${GREEN}[2/4] Running YAPF (Formatter)...${NC}"
# -i: in-place edit
# -r: recursive
# -p: parallel processing (faster)
yapf -i -r -p backend/
if [ $? -ne 0 ]; then
    echo -e "${RED} YAPF failed to format code.${NC}"
    exit 1
fi

# 3. Run Flake8 (Linter)
echo -e "\n${GREEN}[3/4] Running Flake8 (Linter)...${NC}"
flake8 backend/
if [ $? -ne 0 ]; then
    echo -e "${RED} Flake8 failed. Please fix style errors.${NC}"
    exit 1
fi

# 4. Run Mypy (Type Checker)
echo -e "\n${GREEN}[4/4] Running Mypy (Type Checker)...${NC}"
mypy backend/
if [ $? -ne 0 ]; then
    echo -e "${RED} Mypy failed. Please fix type errors.${NC}"
    exit 1
fi

# 5. Run Pytest (Unit Tests)
echo -e "\n${GREEN}[5/5] Running Pytest (Unit Tests)...${NC}"
python -m pytest backend/tests
if [ $? -ne 0 ]; then
    echo -e "${RED} Tests failed. Please fix the bugs.${NC}"
    exit 1
fi

echo -e "\n${GREEN} SUCCESS! All checks passed. You are ready to commit.${NC}"
exit 0