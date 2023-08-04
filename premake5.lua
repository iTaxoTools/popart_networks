workspace("Popart_Networks")
	configurations({"debug", "release"})

	newoption({
		trigger = "kind",
		category = "Custom",
		description = "Kind of binary when building",
		default = "shared",
		allowed = {
			{"exe", "Executable"},
			{"static", "Static library"},
			{"shared", "Shared library"},
		}
	})
	newoption({
		trigger = "disableintnj",
		category = "Custom",
		description = "Disable Integer NJ Network from popart"
	})
	newoption({
		trigger = "includedirs",
		category = "Custom",
		description = "List of include directories separated by semicolons"
	})
	newoption({
		trigger = "libdirs",
		category = "Custom",
		description = "List of library directories separated by semicolons"
	})
	newoption({
		trigger = "target",
		category = "Custom",
		description = "The produced library is copied here"
	})
	newoption({
		trigger = "arch",
		category = "Custom",
		description = "Target architecture",
		default = "x86_64",
		allowed = {
			{"x86", "x86/x32, 32 bit architecture"},
			{"x86_64", "x86_64/x64, 64 bit architecture"},
			{"arm64", "arm64, 64 bit architecture"},
		}
	})
	newoption({
		trigger = "pythonversion",
		category = "Custom",
		description = "Python version to link against for non-Windows systems",
		default = "3.11"
	})
	newoption({
		trigger = "nopython",
		category = "Custom",
		description = "Disable Python bindings"
	})

	project("popart_networks")
		filter("options:kind=exe")
			kind("ConsoleApp")
		filter("options:kind=static")
			kind("StaticLib")
		filter("options:kind=shared")
			kind("SharedLib")
		filter("options:*")
		language("C++")
		cppdialect("C++17")
		architecture(_OPTIONS["arch"])

		includedirs({
			"src/itaxotools/_popart_networks/include",
			"src/popart/src",
		})

		if _OPTIONS["includedirs"] then
			for path in string.gmatch(_OPTIONS["includedirs"], "[^;]+") do
			  includedirs { path }
			end
		end

		if _OPTIONS["libdirs"] then
			for path in string.gmatch(_OPTIONS["libdirs"], "[^;]+") do
			  libdirs { path }
			end
		end

		filter({"system:not windows"})
			includedirs("/usr/include/python" .. _OPTIONS["pythonversion"])
		filter({})
		files({
			"src/itaxotools/_popart_networks/src/*.cpp",
			--"popart/src/testgraphs.cpp"
		})
		filter({"not options:nopython", "system:windows"})
			removefiles({
				"src/itaxotools/_popart_networks/src/python_wrapper.cpp",
			})
		filter({"options:disableintnj"})
			defines({"DISABLE_INTNJ"})
		filter({})

		location("build")
		--targetdir("build/bin/${cfg.buildcfg}")
		--targetname("popart_networks")
		filter({})
		links({
			"popart"
		})
		filter({"not options:nopython", "system:windows"})
			links("python3")
		filter({"not options:nopython", "system:not windows"})
			links("python" .. _OPTIONS["pythonVersion"])
		filter({})
		--pic("On")
		linkoptions({})
		warnings("Extra")
		filter({"not system:windows"})
			buildoptions({"-pedantic"})
			disablewarnings({
				"unused-parameter",
				"comment",
				"catch-value",
				"sign-compare"
			})

		filter({"configurations:debug"})
			defines({"DEBUG"})
			optimize("Debug")
			symbols("On")

		filter({"configurations:release"})
			defines({"NDEBUG"})
			optimize("Full")
			--symbols("Off")

		if _OPTIONS["target"] then
			filter({"not system:windows"})
				postbuildcommands {
					"{COPYFILE} %{cfg.buildtarget.relpath} " .. _OPTIONS["target"]
				}
			filter({})
			filter({"system:windows"})
				postbuildcommands {
					"{COPYFILE} $(TargetPath) " .. _OPTIONS["target"]
				}
			filter({})
		end


	project("popart")
		kind("StaticLib")
		language("C++")
		cppdialect("C++17")
		architecture(_OPTIONS["arch"])

		includedirs({
			"src/popart/src/networks",
			"src/popart/src/tree",
			"src/popart/src/seqio",
		})
		files({
			"src/popart/src/networks/*.cpp",
			"src/popart/src/tree/*.cpp",
			"src/popart/src/seqio/*.cpp",
		})

		filter({"options:disableintnj"})
			removefiles({"src/popart/src/networks/IntNJ.cpp"})
		filter({})
		filter({"not options:disableintnj"})
			links({"lpsolve55"})
		filter({})

		location("build")
		--pic("On")
		linkoptions({})
		warnings("Extra")
		filter({"not system:windows"})
			--buildoptions({"-pedantic"})
			disablewarnings({
				"unused-parameter",
				"sign-compare",
				"deprecated-copy",
				"mismatched-new-delete",
				"maybe-uninitialized",
				"char-subscripts",
				"misleading-indentation",
				"implicit-fallthrough",
				"unused-but-set-variable",
				"unused-result",
			})

		filter({"configurations:debug"})
			defines({"DEBUG"})
			optimize("Debug")
			symbols("On")

		filter({"configurations:release"})
			defines({"NDEBUG"})
			optimize("Full")
			--symbols("Off")
