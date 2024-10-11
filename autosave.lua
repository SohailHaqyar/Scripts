local function process_build_output(data)
	local quickfix_list = {}

	for _, line in ipairs(data) do
		-- Strip ANSI color codes
		local clean_line = line:gsub("\27%[[0-9;]*m", "")

		-- Parse the file path, line number, and column number
		local file, line_num, col_num = clean_line:match("^Error:(%S+):(%d+):(%d+)")

		if file and line_num and col_num then
			-- Add the parsed information to the quickfix list
			table.insert(quickfix_list, {
				filename = file,
				lnum = tonumber(line_num),
				col = tonumber(col_num),
				text = "Error in file",
			})
		end
	end

	-- Set the quickfix list with the parsed errors
	if #quickfix_list > 0 then
		vim.fn.setqflist(quickfix_list, "r")
    print("Refreshed list")
	else
		print("No errors found.")
	end
end

vim.api.nvim_create_autocmd("BufWritePost", {
	pattern = "/home/kaka/work/cloud-portal/src/*",
	group = vim.api.nvim_create_augroup("cloudPortalStalker", {
		clear = true,
	}),
	callback = function()
		local cmd = [[yarn build 2>&1 | awk '/^Error: / {print $1 $2}']]

		vim.fn.jobstart(cmd, {
			stderr_buffered = true,
			stdout_buffered = true,

			on_stdout = function(_, data)
				if data then
					process_build_output(data)
				end
			end,

			on_stderr = function(_, data)
				if data then
					process_build_output(data)
				end
			end,

			on_exit = function(_, exit_code)
				if exit_code == 0 then
					print("Build success...")
				else
          print("Failed build..")
				end
			end,
		})
	end,
})
