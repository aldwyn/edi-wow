class PostfixCalculator:

	def __init__(self):
		self.operators = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 4, ')': 4}


	def converter(self, expr):
		prefix_expression = expr
		tokens = prefix_expression.split()
		checker = 0
		parenthesis = 0
		is_valid_input = True
		for x in xrange(len(tokens)):
			if tokens[x] == '(':
				parenthesis += 1
			elif tokens[x] == ')':
				parenthesis -= 1
			elif self.is_number(tokens[x]):
				checker += 1
			else:
				checker -= 1

			if checker < 0 or checker > 1:
				is_valid_input = False
				break

		if not is_valid_input or parenthesis != 0 or checker != 1:
			return None

		postfix_expression = ''
		stack = []
		isValid = True

		for x in xrange(len(tokens)):
			if tokens[x] == '(':
				stack.append(tokens[x])
			elif tokens[x] == ')':
				while True:
					if len(stack) == 0:
						isValid = False
						break
					elif stack[len(stack)-1] == '(':
						stack.pop()
						break
					else:
						postfix_expression += (stack.pop() + ' ')
				if not isValid:
					break
			elif tokens[x] in self.operators:
				if len(stack) == 0 or stack[len(stack)-1] == '(':
					stack.append(tokens[x])
				else:
					top = stack[len(stack)-1]
					if self.operators[top] == self.operators[tokens[x]]:
						postfix_expression += (stack.pop() + ' ')
					elif self.operators[top] > self.operators[tokens[x]]:
					 	while self.operators[stack[len(stack)-1]] >= self.operators[tokens[x]]:
					 		postfix_expression += (stack.pop() + ' ')
					 		if len(stack) < 1 or stack[len(stack)-1] == '(':
					 			break
					stack.append(tokens[x])
			else:
				postfix_expression += (tokens[x] + ' ')

		while len(stack) > 0 and isValid:
			top = stack.pop()
			if top == "(" or top == ")":
				isValid = False
				break
			postfix_expression += (top + ' ')

		if isValid:
			return self.calculator(postfix_expression)
		else:
			# print 'Invalid infix'
			return None


	def calculator(self, post_expr):
		postfix_expression = post_expr
		tokens = postfix_expression.split()
		stack = []
		isValid = True

		for x in xrange(len(tokens)):
			if tokens[x] not in self.operators:
				stack.append(float(tokens[x]))
			else:
				if len(stack) > 1:
					total = 0
					num1 = stack.pop()
					num2 = stack.pop()
					if tokens[x] == '+':
						total = num2+num1
					elif tokens[x] == '-':
						total = num2-num1
					elif tokens[x] == '*':
						total = num2*num1
					elif tokens[x] == '/':
						total = num2/num1
					elif tokens[x] == '^':
						total = pow(num2, num1)
					stack.append(total)
				else:
					isValid = False
					break
		if isValid and len(stack) == 1:
			answer = stack.pop()
			return answer
		else:
			# print 'Invalid postfix'
			return None


	def is_number(self, string):
		try:
			float(string)
			return True
		except:
			return False


if __name__ == "__main__":
	pfc = PostfixCalculator()